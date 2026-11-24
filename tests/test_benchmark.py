import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import benchmark


class FakeModel:
    def __init__(self, result):
        self.result = result
        self.requests = []

    def count(self, prompt):
        return len(prompt) // 4

    def complete(self, prompt, limit):
        self.requests.append((prompt, limit))
        text = '{"notes":"Check filing rows."}' if prompt.startswith("Find evidence") else json.dumps(self.result)
        return text, self.count(prompt), 16, "completed"


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tasks = {task["id"]: task for task in benchmark.jsonl(benchmark.DATA / "tasks.jsonl")}
        self.keys = {key["id"]: key for key in benchmark.jsonl(benchmark.DATA / "answer_key.jsonl")}
        self.schemas = json.loads((benchmark.DATA / "response_fields.json").read_text())
        self.task = self.tasks["FIN-01"]
        self.key = self.keys["FIN-01"]
        self.schema = self.schemas["FIN-01"]
        self.url = self.task["filings"][0]["url"]
        self.quote = "Total revenues 24,578 and total cost of revenues 20,509"
        self.excerpts = {self.url: self.quote}
        self.answer = {
            "answer": self.key["expected"].copy(), "unit": "USD millions",
            "evidence": [{"url": self.url, "quote": self.quote}],
        }

    def test_task_key_and_prompt_shapes_agree(self):
        self.assertEqual(len(self.tasks), 20)
        self.assertEqual(self.tasks.keys(), self.keys.keys())
        self.assertEqual(self.tasks.keys(), self.schemas.keys())
        for identity, task in self.tasks.items():
            self.assertEqual(set(self.schemas[identity]["fields"]), self.keys[identity]["expected"].keys())
            self.assertEqual(set(self.schemas[identity]["sections"]), {f["company"] for f in task["filings"]})

    def test_retrieval_preserves_rows_and_omits_hidden_metadata(self):
        with TemporaryDirectory() as directory:
            cache = Path(directory)
            path = benchmark.filing_path(cache, self.task["filings"][0])
            path.write_text(
                '<html><body><ix:header><ix:hidden>Hidden metadata</ix:hidden></ix:header>'
                '<div>Consolidated Statements of Operations</div><table><tr>'
                '<td><div>Total revenues</div></td><td><div>24,578</div></td></tr>'
                '<tr><td>Loss from operations</td><td>(69)</td></tr></table></body></html>'
            )
            excerpt = benchmark.retrieve(self.task, self.schema, cache)[self.url]
            self.assertIn("Total revenues | 24,578", excerpt)
            self.assertNotIn("Hidden metadata", excerpt)

    def test_value_and_evidence_fail_independently(self):
        self.assertEqual(benchmark.score_response(self.answer, self.excerpts, self.key), (True, True))
        self.answer["unit"] = "USD thousands"
        self.assertEqual(benchmark.score_response(self.answer, self.excerpts, self.key), (False, True))
        self.answer["unit"] = "USD millions"
        self.answer["evidence"][0]["quote"] = "Invented evidence passage"
        self.assertEqual(benchmark.score_response(self.answer, self.excerpts, self.key), (True, False))

    def test_signs_booleans_and_tolerances(self):
        self.assertTrue(benchmark.matches(-25912, "(25,912)", 0))
        self.assertTrue(benchmark.matches(24.59, 24.595, 0.005))
        self.assertFalse(benchmark.matches(24.59, 24.596, 0.005))
        self.assertFalse(benchmark.matches(False, 0, 0))
        self.assertFalse(benchmark.matches(10, float("nan"), 0))

    def test_both_configurations_respect_budget_and_exclude_key(self):
        for configuration, calls in (("single", 1), ("team", 2)):
            with self.subTest(configuration=configuration):
                client = FakeModel(self.answer)
                row = benchmark.attempt(client, self.task, self.schema, self.excerpts, configuration, 1200)
                self.assertIsNone(row["error"])
                self.assertEqual(len(row["calls"]), calls)
                spent = 0
                for (prompt, limit), usage in zip(client.requests, row["calls"]):
                    self.assertIn(self.quote, prompt)
                    self.assertNotIn(self.key["rationale"], prompt)
                    self.assertLessEqual(spent + client.count(prompt) + limit, 1200)
                    spent += usage["input_tokens"] + usage["output_tokens"]
        client = FakeModel(self.answer)
        row = benchmark.attempt(client, self.task, self.schema, self.excerpts, "team", 10)
        self.assertIn("token budget", row["error"])
        self.assertEqual(client.requests, [])

    def test_paired_report_and_review_template(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)
            run_path = path / "run.jsonl"
            review = path / "review.csv"
            rows = [
                dict(benchmark.attempt(FakeModel(self.answer), self.task, self.schema,
                                       self.excerpts, config, 1200),
                     trial=1, model="fake", token_budget=1200)
                for config in benchmark.CONFIGURATIONS
            ]
            run_path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            args = argparse.Namespace(run=run_path, review=None, review_template=review, output=None,
                                      input_rate=1.0, output_rate=2.0)
            with redirect_stdout(io.StringIO()) as output:
                benchmark.score(args, self.keys)
            report = json.loads(output.getvalue())
            self.assertEqual(report["scoring"], "provisional_automated")
            self.assertEqual(report["summary"]["team"]["joint_accuracy"], 1.0)
            with self.assertRaisesRegex(ValueError, "reviewer"):
                benchmark.read_reviews(review, rows, run_path)
            review.write_text(review.read_text().replace(",,,\n", ",Reviewer,yes,no\n"))
            args.review_template, args.review = None, review
            with redirect_stdout(io.StringIO()) as output:
                benchmark.score(args, self.keys)
            report = json.loads(output.getvalue())
            self.assertEqual(report["scoring"], "human_reviewed")
            self.assertEqual(report["summary"]["team"]["joint_accuracy"], 0.0)


if __name__ == "__main__":
    unittest.main()
