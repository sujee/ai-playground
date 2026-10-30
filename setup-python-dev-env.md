# Setup a Local Python Dev Environment

We will use [uv](https://docs.astral.sh/uv/) to manage Python environments. It is fast, and each module in this repo is its own self-contained uv project.

## Step-1: Install uv

Install uv by following the [guide here](https://docs.astral.sh/uv/getting-started/installation/).

Verify the install

```bash
uv --version
```

## Step-2: Get the repo

```bash
git  clone  https://github.com/sujee/ai-playground
```

```bash
cd  ai-playground
```

## Step-3: Setup a project

Every module directory (`tokenizers`, `embeddings`, `vector-db`, `llm-intro`, `chat-app-1`, `rag/rag-1`, `rag/rag-2`) is its own uv project.

`cd` into the project directory and sync its environment

```bash
cd  tokenizers

uv  sync
```

This creates a local `.venv` with all the required libraries.  Do this once per project.

**Note**: Jupyter (`jupyterlab`, `ipykernel`) is a dev tool — it lives in the `dev` dependency group in `pyproject.toml`, and `uv sync` installs it by default.  To sync only the runtime libraries

```bash
uv  sync  --no-dev
```

## Step-4: Setup API keys (.env)

Each project that needs API keys has a `.env.sample` file.  Copy it into `.env` in the project directory and populate your keys.

```bash
cp  .env.sample  .env
```

## Step-5: Start Jupyter

From the project directory

```bash
uv  run  jupyter  lab
```

Jupyter is installed from the project's `dev` dependency group (see Step-3).  It will automatically use the project's environment.

## Running the chat app

The `chat-app-1` project has no notebooks.  Run it with

```bash
uv  run  streamlit  run  chat_app1_openai.py
```

## Troubleshooting

### If libraries are not loading in Jupyter

Make sure you started Jupyter with `uv run jupyter lab` from the project directory — that guarantees the notebook kernel uses the project's environment.
