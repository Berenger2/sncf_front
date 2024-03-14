import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

from services import (nombre_gares_total, elements_par_page, nombre_categories_total,
                      nombre_objets_total, all_datas, search_objects_by_station,
                      search_objects_by_category, types)

st.set_page_config(page_title="SNCF :: Objets trouvé", page_icon="✏️", layout="wide")
st.write("# SNCF :: Tableau de visualisation des objets 🚉️")
st.sidebar.image("./img/logo.png", use_column_width=True)

load_dotenv()

API_ENDPOINT = str(os.getenv("API_ENDPOINT"))

st.title("Tableau de bord")


col1, col2 = st.columns(2)

with st.expander("## Statistiques"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Nombre total de gares", value=nombre_gares_total)
    with col2:
        st.metric(label="Nombre d'objets", value=nombre_objets_total)
    with col3:
        st.metric(label="Nombre de catégories", value=nombre_categories_total)

col1, col2 = st.columns(2)

with col1:
    st.title("Liste des objets")

    datas = all_datas
    if datas.status_code == 200:
        try:
            data = datas.json()
            selected_columns = {
                "_id": "ID",
                "date": "Date",
                "gc_obo_gare_origine_r_name": "Gare Origine",
                "gc_obo_nature_c": "Nature",
                "gc_obo_type_c": "Type"
            }

            page = st.number_input('Page', min_value=1, value=1)
            start_idx = (page - 1) * elements_par_page
            end_idx = start_idx + elements_par_page

            df = pd.DataFrame(data, columns=selected_columns.keys())
            df.rename(columns=selected_columns, inplace=True)

            st.write("DataFrame des objets depuis l'API :")
            st.dataframe(df[start_idx:end_idx])

            total_pages = len(df) // elements_par_page + 1
            st.write(f'Page {page}/{total_pages}')
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")

    else:
        st.error(f"Erreur lors de la récupération des données depuis l'API. Code de statut : {datas.status_code}")

with col2:

    st.title("Ajouter un nouvel objet trouvé")

    date = st.date_input("Date")
    gare_origine = st.text_input("Gare Origine")
    nature = st.text_input("Nature")
    type_objet = st.text_input("Type d'objet")

    if st.button("Ajouter"):
        date_str = date.strftime('%Y-%m-%d')
        data = {
            "date": date_str,
            "gc_obo_gare_origine_r_name": gare_origine,
            "gc_obo_nature_c": nature,
            "gc_obo_type_c": type_objet
        }
        add_data = requests.post(API_ENDPOINT + '/add_data', json=data)
        if add_data.status_code == 200:
            st.success("Objet ajouté avec succès!")
        else:
            st.error("Une erreur s'est produite lors de l'ajout de l'objet.")

st.title("Recherche d'objets par gare")
station_input = st.text_input("Entrez le nom de la gare")

if st.button("Rechercher"):
    if not station_input:
        st.error("Veuillez fournir le nom de la gare.")
    else:
        objects = search_objects_by_station(station_input)
        if objects:
            st.write("Résultats de la recherche :")

            data_gar = objects
            selected_columns = {
                "date": "Date",
                "gc_obo_nature_c": "Nature",
                "gc_obo_type_c": "Type"
            }

            df_gare = pd.DataFrame(data_gar, columns=selected_columns.keys())
            df_gare.rename(columns=selected_columns, inplace=True)
            st.dataframe(df_gare)

        else:
            st.write("Aucun objet trouvé pour cette gare.")

categories = types

st.title("Recherche d'objets par catégorie")
selected_categories = st.selectbox("Sélectionnez une catégorie :", categories, key=f"selectbox_1")

if st.button("Filtrer"):
    objects = search_objects_by_category(selected_categories)
    if objects:
        st.write("Résultats de la recherche :")
        data_res = objects
        selected_columns = {
            "date": "Date",
            "gc_obo_gare_origine_r_name": "Gare Origine",
            "gc_obo_nature_c": "Nature",
        }

        df_obj = pd.DataFrame(data_res, columns=selected_columns.keys())
        df_obj.rename(columns=selected_columns, inplace=True)
        st.dataframe(df_obj)
    else:
        st.write("Aucun objet trouvé pour cette catégorie.")

st.title("Visualisation des objets par catégorie")
selec_cat = st.selectbox("Sélectionnez une catégorie :", categories, key=f"selectbox_2")

if st.button("Généger histogramme"):
    objects = search_objects_by_category(selec_cat)
    if objects:
        category_counts_ = {}
        for obj in objects:
            category = obj.get('gc_obo_nature_c', categories)
            category_counts_[category] = category_counts_.get(category, 0) + 1

        plt.bar(category_counts_.keys(), category_counts_.values())
        plt.xlabel("Catégorie")
        plt.ylabel("Nombre d'objets")
        plt.title("Histogramme des objets par catégorie")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)
    else:
        st.write("Aucun objet trouvé pour cette catégorie.")

