##
# Requêtes sur l'API TMDB 
##

# Librairies
import tmdbsimple as tmdb
import requests
import json
from tqdm import tqdm

# Clé de l'API TMDB pour avoir l'autorisation de faire des requêtes
tmdb.API_KEY = '4774cbd440f2c43e617d50c2b663cfcf'

# On récupère les données relatives aux films produits entre 2015 et 2018
list_years = [i for i in range(2015,2019)] # années allant de 2015 à 2018
films_id = [] # Pour stocker les identifiants uniques des films
films_infos = [] # Pour stocker les informations générales sur les films
films_credits = [] # Pour stocker les castings / équipes des films

# Récupération des identifiants uniques
print("\nRequest ID :")
for year in tqdm(list_years) :
    new_results = True
    page = 1
    while new_results :
        res = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&api_key="+tmdb.API_KEY+f"&year={year}"+f"&page={page}").json()
        new_results = res.get("results", [])
        films_id.extend(new_results)
        page += 1

films_id = [film["id"] for film in films_id] # On ne conserve que les identifiants

# On doit effectuer une autre série de requêtes à partir des identifiants précédents
# pour avoir accès aux informations et aux crédits (casting + équipe de tournage / production)
print("\nRequest informations :")
for id in tqdm(films_id) : 
    url_infos = "https://api.themoviedb.org/3/movie/"+str(id)+"?api_key="+tmdb.API_KEY
    url_credits = "https://api.themoviedb.org/3/movie/"+str(id)+"/credits?api_key="+tmdb.API_KEY
    films_infos.append(requests.get(url_infos).json())
    films_credits.append(requests.get(url_credits).json())

# Sauvegarde des données
with open("/Users/joshuawolff/Documents/Github/TMDB_movies_project/films_infos.json", "w") as fout:
    json.dump(films_infos, fout)
with open("/Users/joshuawolff/Documents/Github/TMDB_movies_project/films_credits.json", "w") as fout:
    json.dump(films_credits, fout)

print("\n--------- END ---------\n")

#with open(r"/Users/joshuawolff/Desktop/films_infos.json", "r") as read_file:
#    data = json.load(read_file)