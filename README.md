# SEC Finance Agent Eval

[![Offline tests](https://github.com/ohjeffkuston/sec-finance-agent-eval/actions/workflows/tests.yml/badge.svg)](https://github.com/ohjeffkuston/sec-finance-agent-eval/actions/workflows/tests.yml)

A reproducible benchmark for testing whether one agent or two can answer SEC filing questions more accurately under the same total token budget. The pilot contains 20 tasks drawn from original Form 10-Ks for Tesla, 3D Systems, Apple, and Microsoft.

**[Read all 20 worked solutions](SOLUTIONS.md)** · [Browse the task prompts](data/tasks.jsonl) · [Run the benchmark](#run-the-benchmark)

## See a solution in action

**Reconcile restricted cash at 3D Systems.** The balance sheet showed $133.665 million in cash and cash equivalents. The filing's cash flow footnote disclosed another $0.952 million in restricted cash. Adding the two reconciles to $134.617 million on the cash flow statement. The checker tests the amount, units, and whether the response cites a passage from the filing. [Worked solution and source](SOLUTIONS.md#3d-systems-fy2019)

Other tasks test fiscal-year selection, financial ratios, multi-statement calculations, non-GAAP adjustments, and when the available data is insufficient to answer.

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

## Run on GitHub Actions

The **Live benchmark** workflow starts only when dispatched manually. In the repository's
**Settings → Secrets and variables → Actions**, add these repository secrets:

- `OPENAI_API_KEY` — an API key for your OpenAI project.
- `SEC_USER_AGENT` — your name or organization followed by a contact email.

Open **Actions → Live benchmark → Run workflow** and choose **smoke** first. It
runs both configurations on FIN-01 with up to three model calls. After the
smoke test succeeds, choose **pilot** for all 20 tasks and three trials per
configuration. Both use the pinned GPT-5.4 mini snapshot and a 16,000-token
cap per attempt. Review the project's API pricing before starting.

Download the workflow's artifact for the raw attempts, provisional report,
and human-review CSV. Keep in mind that the repository is public. Results
artifacts include public filing excerpts and model outputs and expire after seven days.

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

The offline tests pass. Live model trials and human answer-key sign-off are pending. The worked solutions above are the expected answers for the pilot.

| Configuration | Answer accuracy | Evidence accuracy | Joint accuracy | Median latency | Estimated cost per joint pass |
| --- | --- | --- | --- | --- | --- |
| Single agent | Pending | Pending | Pending | Pending | Pending |
| Two agents | Pending | Pending | Pending | Pending | Pending |

## Repository contents

- [SOLUTIONS.md](SOLUTIONS.md) shows the expected answers, calculations, and filing sources for all 20 tasks.
- `data/tasks.jsonl` contains prompts and SEC filing URLs.
- `data/response_fields.json` contains response field names, unit labels, and filing passage selectors.
- `data/answer_key.jsonl` contains the draft key and supporting evidence locations. The runner does not read this file when generating answers.
- `benchmark.py` provides the cache, paired runner, checker, and review workflow.
- `tests/` runs offline and uses simulated model responses.

[SEC EDGAR access guidance](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) · [OpenAI input token counting](https://developers.openai.com/api/docs/guides/token-counting)
