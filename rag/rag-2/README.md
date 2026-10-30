# RAG Example 2 - Query a Website

In this lab, we will 

- download a website, 
- index the files
- and query them

## Setup

```bash
uv  sync
```

Copy `.env.sample` to `.env` and fill in your API keys

```bash
cp  .env.sample  .env
```

## Step-1: Query a Web site

This example shows 

- how to crawl a website 
- index it
- and query using an LLM

We use `llama-index` framework

Code : [query_a_website.ipynb](query_a_website.ipynb)

## Other Approaches

- crawl the site
- process the pages (cleanup ..etc)
- save the pages to a vector database
- Then query using vector db + LLM


Here is the code that downlaods the site and saves it to Milvus db : [download_and_save_to_db.ipynb](download_and_save_to_db.ipynb)

And query code using Milvus + LLM : [query_from_db.ipynb](query_from_db.ipynb)