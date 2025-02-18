from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    [{"host": 'elasticsearch', "port": 9200, "scheme": "https"}], 
    timeout=30, 
    max_retries=10, 
    retry_on_timeout=True
)
index_schema = {
    "Poster_Link": {"type": "keyword", "null_value": "null"},
    "Series_Title": {"type": "keyword", "null_value": "null"},
    "Released_Year": {"type": "keyword", "null_value": "FALSE"},
    "Certificate": {"type": "keyword", "null_value": "null"},
    "Runtime": {"type": "keyword", "null_value": "null"},
    "Genre": {"type": "keyword", "null_value": "null"},
    "IMDB_Rating": {"type": "keyword", "null_value": "null"},
    "Overview": {"type": "keyword", "null_value": "null"},
    "Meta_score": {"type": "keyword", "null_value": "null"},
    "Director": {"type": "keyword", "null_value": "null"},
    "Star1": {"type": "keyword", "null_value": "null"},
    "Star2": {"type": "keyword", "null_value": "null"},
    "Star3": {"type": "keyword", "null_value": "null"},
    "Star4": {"type": "keyword", "null_value": "null"},
    "No_of_Votes": {"type": "keyword", "null_value": "null"},
    "Gross": {"type": "keyword", "null_value": "null"},
}

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "rebuilt_persian": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "decimal_digit",
                        "persian_normalization",
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {}
    }
}

for field_name, config in index_schema.items():
    index_settings["mappings"]["properties"][field_name] = {}
    for cfg_name, cfg_value in index_schema[field_name].items():
        if cfg_name != "type":   
            index_settings["mappings"]["properties"][field_name][cfg_name] = cfg_value

es.indices.create(index='movies', ignore=400, body=index_settings)

with open('./movies.json') as f:
    lines = f.readlines()

data = [json.loads(line) for line in lines]

for index, record in enumerate(data):
    if index % 2 == 1:
        es.index(index='movies', body=record)
