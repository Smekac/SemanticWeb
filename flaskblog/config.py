import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data/')
MODELS_DIR = os.path.join(ROOT_DIR, 'models/')

""" 
BOOKS_PATH = os.path.join(DATA_DIR, 'books.csv')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')
BOOK_VECTORS_PATH = os.path.join(MODELS_DIR, 'book_vectors.pkl')
"""

SPARQL_SERVER_URL = os.environ.get('SPARQL_SERVER_URL', default='http://localhost:3030/test/')
ONTOLOGY_URI = os.environ.get('ONTOLOGY_URI', default='<http://www.semanticweb.org/stojk/ontologies/2019/6/untitled-ontology-7#>')
