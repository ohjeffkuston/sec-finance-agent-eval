# SEC Finance Agent Eval

Can a two-agent workflow answer SEC filing questions more accurately than a single agent under the same total model token budget?

This development pilot contains 20 tasks using four original Form 10-Ks from Tesla, 3D Systems, Apple, and Microsoft. Tasks cover fiscal periods, units, signs, ratios, statement reconciliations, footnotes, unsupported premises, and cross-company comparisons.

## Run the benchmark

Python 3.11+ is sufficient. No packages need to be installed. Live trials require an OpenAI API key and a model available to your account that supports JSON mode and the Responses input token counting endpoint. Set billing and usage controls in your OpenAI project before starting a live trial.

```bash
python3 -m unittest discover -s tests -v
export SEC_USER_AGENT='Your Name contact@example.com'
python3 benchmark.py fetch

# Load OPENAI_API_KEY from your secret manager or shell.
# Set MODEL to the OpenAI model ID you want to test.
python3 benchmark.py run --model "$MODEL" --task FIN-01 --trials 1 --output runs/smoke.jsonl
python3 benchmark.py run --model "$MODEL" --trials 3 --budget 16000 --output runs/baseline.jsonl
python3 benchmark.py score runs/baseline.jsonl --review-template runs/review.csv
```

Use your own name or organization and contact email in the SEC User-Agent. Downloads are cached and spaced out. The run command reads the cached filings, gives each configuration the same curated excerpts from those filings, and writes paired attempt records. It refuses to overwrite an existing run file. A full three-repeat pilot makes up to 180 generation calls plus token count requests. The one-task smoke run makes up to three generation calls.

## Review and score

1. Review `data/answer_key.jsonl` against the SEC filings. Check expected values, units, signs, periods, tolerances, and the evidence required to support each answer. Correct anything needed and commit the reviewed key before scoring.
2. Open the raw run file and the review CSV. Fill in the reviewer name and mark `answer_ok` and `evidence_ok` with `yes` or `no` for each attempt. For answer credit, require all requested fields, units, and meaningful parts of the explanation. For evidence credit, require the correct filing and passages that support each required input or conclusion. A copied but irrelevant quote fails evidence review.
3. Run the reviewed scoring command. Review rows are bound to hashes of the raw run and answer key. Regenerate the template if the reviewed key or run changes.

```bash
python3 benchmark.py score runs/baseline.jsonl --review runs/review.csv --output runs/report.json
```

Optional `--input-rate` and `--output-rate` flags take standard dollars per million tokens for the selected model. Cost is an estimate at those rates and does not incorporate cache discounts, additional service charges, or failed requests with unavailable usage. The provisional scorer checks numeric and categorical answer fields, units, and whether quotes are present in each required filing excerpt. Human review checks evidence relevance and explanations.

## Experiment design

| Configuration | Model calls per attempt |
| --- | --- |
| Single agent | One call reads the question and filing excerpts and produces a final answer. |
| Two agents | An analyst proposes inputs and calculations. A verifier gets the same excerpts and analyst notes and produces the final answer. |

Both configurations receive the same model, filing excerpts, answer field names, and total per-task cap across input and output. The runner counts the input before each generation and limits the output by the remaining shared budget. Repeated filing excerpts in the team workflow count toward its cap. Actual usage can differ. The logged latency includes token preflights and generation. Failed and truncated final attempts stay in the denominator.

This benchmark measures reasoning and citation against curated passages. Filing discovery and open-web retrieval are outside this pilot. The 20 tasks reuse public documents and some inputs. Use fresh companies and years for a held-out comparison.

## Results

Live comparison pending human answer-key review and model trials. Local tests exercise the parser, checker, budget allocation and paired reporting.

| Configuration | Answer accuracy | Evidence accuracy | Joint accuracy | Median latency | Estimated cost per joint pass |
| --- | --- | --- | --- | --- | --- |
| Single agent | Pending | Pending | Pending | Pending | Pending |
| Two agents | Pending | Pending | Pending | Pending | Pending |

## Repository contents

- `data/tasks.jsonl` contains prompts and SEC filing URLs.
- `data/response_fields.json` contains response field names, unit labels, and filing passage selectors.
- `data/answer_key.jsonl` contains the draft key and supporting evidence locations. The runner does not read this file when generating answers.
- `benchmark.py` provides the cache, paired runner, checker, and review workflow.
- `tests/` runs offline and uses simulated model responses.

[SEC EDGAR access guidance](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) · [OpenAI input token counting](https://developers.openai.com/api/docs/guides/token-counting)
