#!/usr/bin/env python
# coding: utf-8

# # Application : Meteo en ligne via l’API de OpenWeatherMap
# OpenWeatherMap est un service en ligne qui fournit des données météorologiques, y compris des données météorologiques actuelles, des prévisions et des données historiques aux développeurs de services Web et d'applications mobiles.
# 

# In[1]:


#Image(url= "weather.png")


# In[2]:


#get_ipython().system('pip install termcolor')
#from IPython.display import Image                                                                  
#from IPython.core.display import HTML
import os
import csv
from termcolor import colored, cprint
#os.chdir("C:\\users\\msellami\\PythonTraining\\")


# 
# 
# Dans cet atelier, nous exploitions cette api afin d’extraire les données météorologique sous forme JSON et on le stocke dans un fichier CSV respectant un format bien défini.
# #### Pour cela nous suivons les étapes suivantes
# Depuis 2015, utiliser openweathermap nécessite de s'enregistrer. On s'authentifie ensuite en utilisant une clé. Chaque requête doit sonc être complétée par : &appid=XXXXX où XXX est la valeur de la clé à utiliser. Cette clé est disponible sur Updago.
# Nous allons utiliser le service OpenWeatherMap pour récolter des prévisions météo. Ces prévisions pourront être resservies par un site Web, par exemple.
# Le site http://openweathermap.org propose une API pour récolter les informations qu'il diffuse.
# Prendre connaissance des possibilités de l'API
# La page de documentation de l'API est accessible ici : http://openweathermap.org/api
# #### Voici quelques exemples :
# http://api.openweathermap.org/data/2.5/weather?q=Tunis,Tunisia&appid=XXX
# Remplacez XXX par la clé API. Dans la suite, pensez à ajouter le champ appid=XXX.
# Remplacer ?q=Tunis,Tunisia par la villes et le pays recherchés.
# La commande weather employée ici indique que nous souhaitons obtenir les conditions météo actuelles.
# Le résultat est par défaut fourni au format json. Dans le cas de la commande weather, voici les informations qui sont obtenues : Weather Data
# Il y a bien sûr d'autres commandes disponibles, qu'on trouvera dans la documentation. Notez en particulier la commande forecast qui permet d'obtenir des prévisions.
# ## Outils Python
# #### Accès à l'API
# Comme indiqué dans le cours, nous allons utiliser Python pour interroger openweathermap. Le module requests sera utilisé à la place d'urllib 
# 

# #### Chargement des modules importantes
# 

# In[3]:


import datetime
import json
import urllib.request


# #### Configuration de API et genration de url d'accès à l'API
# Définition d'un fonction qui prend en parametres id de la ville, la ville, le pays pour generer un url respectant l'appel de l'<b>API OpenWeatherMAP</b> et aussi configurer l'APPID recuperé après enregistrement sur le site.
# En effet, l'accès à l'api est effectué soit en utilisant ID de la ville (Tunis) récuperé via la site ( https://openweathermap.org/city/2464470) ou via un fichier json conteant la liste des pays et leur villes accessible via http://bulk.openweathermap.org/sample/city.list.json.gz.
# #### Accès direct avec ID Ville/Pays
# *- http://api.openweathermap.org/data/2.5/weather?id=2464470&mode=json&units=metric&APPID
# #### Accès avec recherche de Ville et Pays
# *-  http://api.openweathermap.org/data/2.5/weather?q=Tunis,Tunisia&mode=json&units=metric&APPID
# 
# Il faut specifier aussi les données sous forme JSON ou XML et l'unité de temperature (°C,F).
# Pour Fahrenheit, on utilise unité=imperial, pour Celsius, on utilise unité= metric, et  par defaut Kelvin. 

# In[4]:


def url_builder(city_id,city_name,country):
    user_api = '4e0f8959dab541379b863bd8868196a6'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    if(city_name!=""):
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' # "http://api.openweathermap.org/data/2.5/weather?q=Tunis,fr
        full_api_url = api + str(city_name) +','+ str(country)+ '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
   
    return full_api_url


# Test cette fonction avec Tunis, Tunisia ou son ID=2464470

# In[5]:


city_name='Tunis'
country='Tunisia'
city_id='2464470'
url=url_builder(city_id,city_name,country)
 
print(colored('API avec Recherche:\n', 'red',attrs=['bold']), colored(url, 'green'))

url=url_builder(city_id,'','')

print(colored('API avec ID\n', 'red',attrs=['bold']), colored(url, 'green'))


# Maintenant on passe à definir une fonction qui permet de récuperer le fichier JSON a partir de cette URL en utilisant <b>urllib.request.urlopen()</b>, <b>str.read.decode('utf-8')</b> pour l'encodage et <b>json.load() </b>pour charger une structire <b>SJON</b> a partir des fichier

# In[6]:


def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


# In[7]:


full_api_url=url_builder(city_id,'','')
data=data_fetch(full_api_url)
print(colored(data, 'yellow',attrs=['bold']))


# #### Gestion des dates
# Le module datetime, qui doit être installé sur vos machines permet de manipuler les dates et les heures. En particulier, il permet de convertir un timestamp en date :

# In[8]:


import datetime
ts = 1543219200.0
print(datetime.datetime.fromtimestamp(ts))


# Toujour dans le module datetime, la méthode datetime.datetime.now() renvoie la date (et l'heure actuelle). On peut aussi construire une date comme ceci :
# 

# In[9]:


d = datetime.datetime(year=2018, month=11,day=26, hour=9, minute=00)


# Une date, obtenue ainsi ou avec now() peut être transformée en timestamp :

# In[10]:


print(d.timestamp())


# ### Convertion et formatage de heure et date
# Definir une fonction qui permet de convertir un timestamp en Heure de la forme HH:MM AM/PM

# In[11]:


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


# ### Extraction des champs à partir des fichiers JSON 
# Mainetant, nous avons besoins de creer une fonction <b>data_organizer</b> qui prend une structure json complexe et créee une dictionnaire de données
# contenant les attributs suivants:
# <b>
#     
# *-city : La ville
#     
# *-country: le pays
# 
# *-temp: Temperature actuelle
# 
# *-temp_max: Temperature temp_max
# 
# *-temp_min :Temperature Min 
# 
# *-humidity ; Humidité
# 
# *-pressure ; Pression
# 
# *-sky       : Etat de Ciel 
# 
# *-sunrise  : Lever du soleil  
#  
#  
# *-sunset : Coucher du soleil 
# 
# *-wind : Vistesse de Vent
# 
# *-wind_deg
# 
# *-dt : Date
# 
# *-cloudiness : Nuageux
# 
# </b>
# 

# In[12]:


def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    print (data)
    return data


# ### Définition d'un fonction d'affichage de données en format lisible 

# In[13]:


def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], m_symbol, data['sky'])
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('Wind Speed: {}, Degree: {}'.format(data['wind'], data['wind_deg']))
    print('Humidity: {}'.format(data['humidity']))
    print('Cloud: {}'.format(data['cloudiness']))
    print('Pressure: {}'.format(data['pressure']))
    print('Sunrise at: {}'.format(data['sunrise']))
    print('Sunset at: {}'.format(data['sunset']))
    print('')
    print('Last update from the server: {}'.format(data['dt']))
    print('---------------------------------------')


# ### Enregistrement des donnnées sous forme CSV
# Maintenant on a besoin d'une fonction qui permet serialiser les données sous forme CSV
# 

# 

# In[28]:


def WriteCSV(data):
    with open('weatherOpenMap.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)


# # Lecture du format CSV – Structure de dictionnaire

# In[29]:


def  ReadCSV():
    try:
    #ouverture de fichier en mode lecture en specifiant le encodage
        with open("weatherOpenMap.csv",'r') as Fichier:
        #lecture – utilisation du parseur csv en specifiant délimiteur
            csv_contenu = csv.reader(Fichier,delimiter=",") 
            reader = csv.DictReader(Fichier)
            dic={}
            for row in reader:
                print (row['city'])
                dic.update(row)
            #fermeture du fichier avec la méthode close()
            Fichier.close()
            return dic
    except IOError:
        print("Fichier n'est pas trouvé")


# # Recuperer des coordonnées des villes à partir de json avec pandas
#   Maintenant on a besoin d'une fonction qui permet recuperer les coordonnées des villesd'un fichier JSON 
#   

# In[30]:


import pandas as pd
import json 
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening json in pandas df

#load json object

def getVilles():
    with open('/city.list.json') as f:
        d = json.load(f)
        villes=pd.DataFrame(d)
        return villes;
    
    


# In[31]:


villes=pd.read_json("city.list.json")
villes
villes.head()


# In[18]:



villes[villes["country"]=='FR']['id']


# ## Programme Principale

# In[24]:


ids_france= list(villes[villes["country"]=='FR']['id'])


# In[33]:


if __name__ == '__main__':
    try:
        for i in range(len(ids_france)):
            city_id = ids_france[i]
            #Generation de l url
            print(colored('Generation de l url ', 'red',attrs=['bold']))
            url=url_builder(city_id,'','')
            #Invocation du API afin de recuperer les données
            print(colored('Invocation du API afin de recuperer les données', 'red',attrs=['bold']))
            data=data_fetch(url)
            data_orgnized=data_organizer(data)
               #Enregistrement des données à dans un fichier CSV 
            WriteCSV(data_orgnized)  
        print("les températures de toutes les villes")
       

    except IOError:
            print('no internet')
            print('seulement'+str(i)+"villes ont pu étre scrapper")
df= pd.read_csv("weatherOpenMap.csv",usecols = [0,2],names =["Ville","Température"],index_col = None)
df.to_csv("weatherOpenMap.csv",index=False)


# # Travail à faire
# * Mettre ce code dans un fichier "Weather.py" et executer le avec l'interpreteur Python
# * rendre ce script executable sous ubuntu/windows
# 
# 
