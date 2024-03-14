import requests
from dotenv import load_dotenv
import os

load_dotenv()
elements_par_page = 10

API_ENDPOINT = str(os.getenv("API_ENDPOINT"))

all_datas = requests.get(API_ENDPOINT + '/datas')


rq_sum = requests.get(API_ENDPOINT + '/sum_object')
if rq_sum.status_code == 200:
    data = rq_sum.json()
    nombre_objets_total = data.get('objects')
else:
    nombre_objets_total = 0

rq_gar_sum = requests.get(API_ENDPOINT + '/sum_gares')
if rq_gar_sum.status_code == 200:
    gares = rq_gar_sum.json()
    nombre_gares_total = gares.get('sum_gares')
else:
    nombre_gares_total = 0

rq_cat_sum = requests.get(API_ENDPOINT + '/sum_types')
if rq_cat_sum.status_code == 200:
    cat_sum = rq_cat_sum.json()
    nombre_categories_total = cat_sum.get('sum_types')
else:
    nombre_categories_total = 0


rq_cat_list = requests.get(API_ENDPOINT + '/types')
if rq_cat_list.status_code == 200:
    cat_list = rq_cat_list.json()
    types = cat_list.get('types')
else:
    types = []


def search_objects_by_station(station):
    try:
        req = requests.get(API_ENDPOINT + '/search', params={'gare': station})
        if req.status_code == 200:
            return req.json().get('objets', [])
        else:
            print(f"Erreur lors de la requête à l'API : {req.status_code}")
            return []
    except Exception as e:
        print(e)
        return []


def search_objects_by_category(category):
    try:
        response = requests.get(API_ENDPOINT+'/search_cat', params={'category': category})
        if response.status_code == 200:
            return response.json().get('objects', [])
        else:
            print(f"Erreur lors de la requête à l'API : {response.status_code}")
            return []
    except Exception as e:
        print(e)
        return []