# Worked SEC filing solutions

Each solution identifies the filing evidence and shows the calculation or judgment. These are the expected answers for the public pilot. Human sign-off on the draft key and live model results are pending.

[Task prompts](data/tasks.jsonl) · [Machine-readable answer key](data/answer_key.jsonl) · [How the benchmark works](README.md#experiment-design)

## Tesla FY2019

[Original Form 10-K](https://www.sec.gov/Archives/edgar/data/1318605/000156459020004475/tsla-10k_20191231.htm), Item 8, Consolidated Statements of Operations.

| Task | Worked solution |
| --- | --- |
| **FIN-01 · Revenue and cost of revenue** | Consolidated revenue was **$24,578 million** and total cost of revenue was **$20,509 million**. Use the FY2019 consolidated totals. |
| **FIN-02 · Operating loss** | Gross profit less operating expenses was $4,069 million − $4,138 million = **−$69 million**. |
| **FIN-03 · Gross margin** | Divide gross profit by revenue. $4,069 million ÷ $24,578 million × 100 = **16.56%**. |
| **FIN-04 · Hypothetical variable costs** | Apply the scenario's assumed 40% ratio to revenue. $24,578 million × 0.40 = **$9,831.2 million**, a hypothetical estimate. |
| **FIN-05 · Gross profit reconciliation** | All amounts are in USD millions. Automotive: 20,821 − 16,398 = **4,423**. Energy: 1,531 − 1,341 = **190**. Services and other: 2,226 − 2,770 = **−544**. The three amounts sum to **4,069**. |
| **FIN-06 · Exact variable costs** | **Insufficient information.** Total cost of revenue does not isolate variable costs. A substantiated variable-cost ratio or a breakdown of fixed and variable costs would be needed. |

## 3D Systems FY2019

[Original Form 10-K](https://www.sec.gov/Archives/edgar/data/910638/000091063820000010/ddd-20191231.htm), Item 8, Consolidated Statements of Cash Flows and Consolidated Balance Sheets.

| Task | Worked solution |
| --- | --- |
| **FIN-07 · Opening and closing cash balances** | The cash flow statement reports 110,919 and 134,617 in USD thousands. Divide each by 1,000 for **$110.919 million opening** and **$134.617 million closing**, both including restricted cash. |
| **FIN-08 · Restricted cash reconciliation** | The balance-sheet cash and equivalents were **$133,665 thousand**. Add **$952 thousand** of restricted cash to reconcile to **$134,617 thousand** on the cash flow statement. Footnote **a** places the restricted cash in **Other assets, net**. |
| **FIN-09 · Cash change before and after FX** | Operating, investing, and financing cash flow sum to 31,581 − 26,872 + 18,700 = **23,409**. Add the **289** FX effect for a reported change of **23,698**, all in USD thousands. |
| **FIN-10 · Incorrect opening balance** | The claim is **false**. FY2019 opened at **$110,919 thousand**. The quoted $136,831 thousand was the **FY2018 opening balance**. |
| **FIN-11 · FY2018 cash change** | Using the FY2018 comparison column, 110,919 − 136,831 = **−$25,912 thousand**. |

## Apple FY2024

[Original Form 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm), Item 8.

| Task | Worked solution |
| --- | --- |
| **FIN-12 · Services share of net sales** | Use the statement of operations or Note 2. Services net sales of $96,169 million ÷ total net sales of $391,035 million × 100 = **24.59%**. |
| **FIN-13 · Current ratio** | From the balance sheet, $152,987 million of current assets ÷ $176,392 million of current liabilities = **0.87×**. |
| **FIN-14 · Tax provision and cash paid** | The income tax provision was **$29,749 million**. Net cash paid for income taxes was **$26,102 million**. The difference was **$3,647 million**. Use the statement of operations or Note 7 for the provision and the cash flow statement's supplemental disclosures for cash paid. |
| **FIN-15 · Revenue from deferred balances** | Note 2 reports $7.7 billion of recognized revenue from the specified deferred balance. That is **$7,700 million** at the reported precision. |

## Microsoft FY2024

[Original Form 10-K](https://www.sec.gov/Archives/edgar/data/789019/000095017024087843/msft-20240630.htm), Item 7 and Item 8.

| Task | Worked solution |
| --- | --- |
| **FIN-16 · FY2023 GAAP-to-adjusted operating income** | Item 7 reconciles **$88,523 million** in GAAP operating income to **$89,694 million** adjusted. The **$1,171 million** difference covers severance, hardware-related impairment, and lease consolidation costs. |
| **FIN-17 · Operating margin change** | Use operating income and revenue from the income statements. (109,433 ÷ 245,122 − 88,523 ÷ 211,915) × 100 = **+2.87 percentage points** from FY2023 to FY2024. |
| **FIN-18 · Free cash flow** | Apply the task's definition to the cash flow statement. $118,548 million in operating cash flow less $44,477 million in property and equipment additions = **$74,071 million**. |

## Apple and Microsoft comparison

Use the [Apple](https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm) and [Microsoft](https://www.sec.gov/Archives/edgar/data/789019/000095017024087843/msft-20240630.htm) originals.

| Task | Worked solution |
| --- | --- |
| **FIN-19 · Operating cash flow less cash capital expenditures** | From Item 8 cash flow statements, Apple: 118,254 − 9,447 = **108,807**. Microsoft: 118,548 − 44,477 = **74,071**. Apple minus Microsoft = **34,736**, all in USD millions. |
| **FIN-20 · Fiscal year-end comparison** | The claim that the dates match is **false**. The covers show Apple ended FY2024 on **2024-09-28** and Microsoft on **2024-06-30**. |
