import os 


## Configuration
class MyConfig:
    pass 

MY_CONFIG = MyConfig ()

### -------- configure input / output ---------------

MY_CONFIG.INPUT_DATA_DIR = "../../data/papers"
MY_CONFIG.COLLECTION_NAME = 'papers'

# MY_CONFIG.INPUT_DATA_DIR = "../../data/fomc"
# MY_CONFIG.COLLECTION_NAME = 'fomc'

# MY_CONFIG.INPUT_DATA_DIR = "../../data/10k"
# MY_CONFIG.COLLECTION_NAME = '10k'


# MY_CONFIG.INPUT_DATA_DIR = "../../data/walmart-reports-1"
# MY_CONFIG.COLLECTION_NAME = 'walmart'

### -------------------------------

### Milvus config
MY_CONFIG.DB_URI = './rag_1.db'  # For embedded instance

## Embedding model
MY_CONFIG.EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
MY_CONFIG.EMBEDDING_LENGTH = 384

## LLM Model
MY_CONFIG.LLM_MODEL = "meta/meta-llama-3-8b-instruct"
