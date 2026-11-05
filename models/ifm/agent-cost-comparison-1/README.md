# Agent Cost Comparison 1

Benchmark a few LLMs on a small data-analysis task and compare their
**cost**, **latency**, **token usage**, and **correctness**.

(Adapted from https://github.com/nebius/token-factory-cookbook/tree/main/agents/agent-cost-comparison-1)

## Models Compared

| Model | Provider | AA Intelligence Index | Run file |
|---|---|---|---|
| moonshotai/Kimi-K3.1-Pro | Nebius Token Factory | 46 | [agent_cost_comparison_nebius.py](agent_cost_comparison_nebius.py) |
| Qwen 3.8 27B | Nebius Token Factory | 20 | [agent_cost_comparison_nebius.py](agent_cost_comparison_nebius.py) |
| K2 Horizon | IFM | 18 | [agent_cost_comparison_ifm.py](agent_cost_comparison_ifm.py) |
| Nemotron 3.5 super VL | Nebius Token Factory | 14 | [agent_cost_comparison_nebius.py](agent_cost_comparison_nebius.py) |


Each model is run as a [deepagents](https://github.com/langchain-ai/deepagents)
filesystem agent with no shell or code-execution tool. The agent must inspect
the input files, reason over their contents, and write `result.json` and
`summary.md` to the workspace output directory.

## Task

The benchmark task is the same for every model:

1. Compare Q1 vs Q2 revenue by region.
2. Find the region with the largest absolute revenue change.
3. Calculate its signed change as Q2 minus Q1.
4. Within that region, find the product with the largest change in the same
   direction as the region's change.
5. Write `/output/result.json` and `/output/summary.md`.

The agent has to do all reasoning and arithmetic itself over the file contents —
there is no code-execution tool available.

## Output format

`result.json` must contain exactly these keys:

```json
{
  "region": "west",
  "change": -60000,
  "primary_product": "widget-b"
}
```

The values above illustrate the required types; each run must use values
calculated from its workspace files.

`summary.md` must contain the `# Sales Analysis` heading and exactly three
bullets with the actual computed values:

```markdown
# Sales Analysis

- Region with the largest revenue change: <actual region>
- Dollar amount of that change (signed): <actual signed change>
- Product that contributed most to the change: <actual product>
```

The angle-bracketed text is instructional. The agent must replace every
placeholder rather than copy it or emit label-only bullets. No Executive
Summary section is required.


## Setup

```bash
uv sync
```

Create a `.env` file in this directory with your Nebius API key:

```bash
NEBIUS_API_KEY=your_nebius_key
IFM_API_KEY=your_ifm_api_keky
```

The script validates the key before making any LLM calls.

## Run

Run the benchmark against the default `data-1` suite:

```bash
# for nebius models
uv run python agent_cost_comparison_nebius.py

# for ifm model
uv run python agent_cost_comparison_ifm.py

```

Use a different data suite:

```bash
# nebius models
uv run python  agent_cost_comparison_nebius.py --data-dir data-2

# ifm models
uv run python  agent_cost_comparison_ifm.py --data-dir data-2
# 
```

For each model, a workspace is created at
`benchmarks/<data-suite>/<model>/` (input is copied in, output is written to
`output/`). Each result is validated against `<data-dir>/expected.json`. Once
all models finish, a comparison table is printed sorted by estimated cost.

Different data suites retain separate artifacts. Rerunning the same suite and
model replaces only that model's existing workspace for that suite.

### Options

| Option | Default | Description |
|---|---|---|
| `--data-dir` | `data-1` | Data suite directory under this folder |
| `--dump-transcript` | off | Write messages to `<workspace>/output/_transcript.json` |

## Configuration

Key configuration values live in `agent_cost_comparison_1.py`:

| Constant | Default | Description |
|---|---|---|
| `AGENT_TIMEOUT` | `300` seconds (5 minutes) | Timeout threshold for each `agent.invoke()` call |
| `MODELS` |  models | Models to benchmark and their pricing |
| `OUTPUT_DATA_DIR` | `output` | Output subdirectory inside each workspace |

Adjust `AGENT_TIMEOUT` if slow runs regularly cross the threshold.


## Validation

The built-in score compares `result.json` with the selected suite's
`expected.json`. It also reports whether `summary.md` exists and is nonempty.
It does not currently validate the summary heading, bullet count, or values;
inspect the generated summary or transcript when verifying a run.

## Sample output

MODEL COMPARISON

| Model                        | AA Idx | Success | Score | Turns | Calls | In Tok | Out Tok | Tot Tok | Time    | Cost ▲    |
|------------------------------|--------|---------|-------|-------|-------|--------|---------|---------|---------|-----------|
| nvidia/Nemotron-3.5-Super-VL | 14     | YES     | 100%  | 7     | 11    | 25,434 | 1,410   | 26,844  | 403.53s | $0.008899 |
| IFM/K2-Horizon-375B-A23B     | 18     | YES     | 100%  | 6     | 11    | 17,515 | 724     | 18,239  | 20.76s  | $0.000000 |
| Qwen/Qwen3.8-27B             | 20     | YES     | 100%  | 6     | 9     | 23,321 | 953     | 24,274  | 5.10s   | $0.013353 |
| moonshotai/Kimi-K3.1-Pro     | 46     | YES     | 100%  | 6     | 10    | 19,407 | 1,217   | 20,624  | 23.78s  | $0.050984 |

## Files

- `agent_cost_comparison_1.py` — configuration, orchestration, and per-model
  execution (parsing, validation, cost metrics, comparison table).
- `utils.py` — workspace setup, usage/cost collection, validation, printing,
  transcript serialization, and invocation helpers.
- `data-1/input/` — source data copied into each model's workspace.
- `data-1/expected.json` — ground-truth answer used for scoring.
- `data-2/` — second input suite and its expected result.
- `benchmarks/<data-suite>/` — per-model run artifacts (gitignored).
