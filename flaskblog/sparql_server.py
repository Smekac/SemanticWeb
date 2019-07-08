from SPARQLWrapper import SPARQLWrapper, JSON
from sqlalchemy import Date

from flaskblog import config
from flaskblog.models import Post


sparql = SPARQLWrapper(config.SPARQL_SERVER_URL)

def get_films(genre_film):
    query = """
    PREFIX uni1: {ontology}
    SELECT ?title 
    WHERE {{ 
    ?film a uni1:Film . ?film uni1:title ?title .
    ?film  uni1:hasGenre ?zanr . 
    ?zanr uni1:name ?imeZanra .
    FILTER(str(?imeZanra) = "{genre_film}")
    }}
    """.format(ontology=config.ONTOLOGY_URI, genre_film=genre_film)

    response = _execute_query(query)
    films = {
        Post(title=item['title']['value']) #  ,date_posted=item['date_posted']['value']
        for item in response
    }
    return films

#def insert_new_film():

def _execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    return response['results']['bindings']


