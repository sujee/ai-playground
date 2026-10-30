# Vector Databases

In this section we will introduce **vector databases**

## Setup

```bash
uv  sync
```

## About Vector Databases

**Tired of Search Engines Missing the Point? Vector Databases to the Rescue!**

Traditional search engines struggle with understanding the true meaning behind your queries. Enter **vector databases**, a revolutionary technology that stores information as numerical representations called **"vectors."** These vectors capture the essence and relationships within data, allowing for incredibly powerful **semantic search**.

Think of it like this: instead of searching for exact keywords, you're searching for **meaning**. 

**Here's what vector databases can do:**

* Find similar images even without tags.
* Discover related documents based on their actual content, not just titles.
* Build recommendation engines that truly understand user preferences.

Here are some popular vector databases:  Pinecone, MongoDb Atlas, Milvus, Chroma

**More about vector databases**

- https://lakefs.io/blog/12-vector-databases-2023/
- https://en.wikipedia.org/wiki/Vector_database

## Vector Search Explained

"Vector Search  represents data as vectors in a high-dimensional space and performs searches based on the similarity between these vectors"

For example, let's say we are searching movie plots.

- A simple **keyword search** could be **'sci-fi'**
- A **vector search** could be **'where humans fight aliens'**

Here is an example.  Notice how the results are not merely keywords.

```text
query : fatalistic sci-fi movies
```

```text
Results: 

1
title: Starship Troopers,
year: 1997
plot: Humans in a fascistic, militaristic future do battle with giant alien bugs in a fight for survival.

2
title: Terminator 3: Rise of the Machines,
year: 2003
plot: A cybernetic warrior from a post-apocalyptic future travels back in time to protect a 19-year old drifter and his future wife from a most advanced robotic assassin and to ensure they both survive a nuclear attack.

3
title: Logan's Run,
year: 1976
plot: An idyllic sci-fi future has one major drawback: life must end at 30.
```

Pretty cool, eh? 😎


## Vector DB: Milvus

[Milvus](https://milvus.io/) is an open-source vector database designed for massive datasets and blazing-fast similarity search.

Milvus can be run in 3 modes:

1. Embedded database (like sqllite) - easy to run
2. As a docker container - on local machine, for dev purposes
3. On the cloud as a cluster - for production use

[A good overview of Milvus (pdf)](https://github.com/sujee/data-prep-kit-examples/blob/main/events/2024-09-21__Milvus-Introduction.pdf)

### Labs

1 - [Milvus quick start](milvus_1_quick_start.ipynb)

2 - [Vector search with Milvus](milvus_2_movie_search.ipynb)

## Vector DB: MongoDB Atlas

Atlas is another easy to use vector db, created by MongoDB. Atlas runs on cloud.

You can sign up for a free account here :  https://www.mongodb.com/cloud/atlas/register

Lab : https://github.com/sujee/mongodb-atlas-vector-search

You can try labs (2) and (3)