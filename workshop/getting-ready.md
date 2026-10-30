# Getting Ready for the Workshop

## Step-1: (Necessary) Basic dev tools

Please have the following tools
- git
- a good editor (VSCode ..etc)

## Step-2: (Necessary) Download LLM Run apps

We will use it to run LLMs locally.

Download one the following:

- [LM Studio](https://lmstudio.ai/)
- [Jan.ai](https://jan.ai/)
- Or any other local LLM UI you like to use.


## Step-2: (Necessary) Setup a Local Python Development Env

Follow [setup-python-dev-env.md](../setup-python-dev-env.md) to setup your local python dev environment.

## Step-3: (Necessary) Sign up for Replicate

Get a **free** account at [replicate](https://replicate.com/home)

💰 Use this [invite](https://replicate.com/invites/a8717bfe-2f3d-4a52-88ed-1356231cdf03) to add some credit to your Replicate account!

(Just to give you an idea of pricing, Replicate charges 5c / 1M input tokens, 25c / 1M output token for model meta/meta-llama-3-8b-instruct)

Once you sign up, **create a token**

The free account will give you a few API calls for free.  That is enough for this workshop.

## Step-4: (Necessary) Create an .env file

Each project has an `.env.sample` file.  Copy it into `.env` in the project directory

```bash
cd  <project-dir>

cp   .env.sample   .env
```

Populate your API keys in `.env` file

## Step-5: (Preferred) Install Docker

Install [Docker](https://www.docker.com/) for your machine.

## Step-6: (Preferred) Get an OPENAI API Key

Sign up for [open ai api](https://openai.com/api/) - if you like to use OpenAI products

## Step-7: (Optional) Sign up for MongoDB Atlas

If you like to use MongoDB Atlas, [sign up and setup MongoDB Atlas](../vector-db/setup-atlas.md)


