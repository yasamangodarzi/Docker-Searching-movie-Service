from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request as request_flask
from walrus import Database
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def movies_system():
    movie_name = request_flask.args.get('movie_name')
    if not movie_name:
        return jsonify({'error': 'لطفاً اسم فیلم خود را ارسال کنید'}), 400
    
    # Connect to Redis
    db = Database('redis', "6379", "0")
    movies_redis_cache = db.cache("movies_redis")
    cache_data = movies_redis_cache.get(movie_name)
    
    if cache_data is not None:
        correct_data = json.loads(cache_data)
        correct_data['type'] = 'REDIS'
        return jsonify(correct_data)

    # Connect to Elasticsearch
    es =Elasticsearch("https://localhost:9200",http_auth=('elastic', '12345'),verify_certs=False)

    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"Series_Title": movie_name}}
                ]
            }
        }
    }
    # headers = {"Content-Type": "application/json"}
    search_result = es.search(index="movies",body=query)

    
    if len(search_result['hits']['hits']) > 0:
        movies_redis_cache.set(key=movie_name, timeout=3600, value=json.dumps(search_result['hits']['hits'][0]['_source']))
        search_result['hits']['hits'][0]['_source']['type'] = 'ELASTICSEARCH'
        return jsonify(search_result['hits']['hits'][0]['_source'])
    
    # Search from API if not found in Redis or Elasticsearch
    url = "https://movies-tv-shows-database.p.rapidapi.com/"
    querystring = {"title": movie_name}
    headers = {
        "Type": "get-movies-by-title",
        "X-RapidAPI-Key": "498ca46fd6msh1cfa36a77c07c1ap1edd88jsn788793953a72",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.json()['search_results'] == 0:
        return jsonify({"result": f"اطلاعات فیلم با نام {movie_name} وجود ندارد"})
    
    querystring = {"movieid": response.json()["movie_results"][0]['imdb_id']}
    headers = {
        "Type": "get-movie-details",
        "X-RapidAPI-Key": "498ca46fd6msh1cfa36a77c07c1ap1edd88jsn788793953a72",
        "X-RapidAPI-Host": "movies-tv-shows-database.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    api_response = response.json()
    del api_response['tagline']
    del api_response['imdb_id']
    del api_response['status']
    del api_response['status_message']
    del api_response['youtube_trailer_key']
    movies_redis_cache.set(key=movie_name, timeout=3600, value=json.dumps(api_response))
    api_response['type'] = 'API'
    return jsonify(api_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
