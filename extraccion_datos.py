import requests
import pandas as pd
import json


    
url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
	"X-RapidAPI-Key": "53ac9a087fmsh84ed2bd05270db2p1d6897jsnf2b9a47f7787",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

myjson = response.json()
myjson_data = myjson['response']

with open('dat\covid_statistics.json','w') as f:
    json.dump(myjson, f, indent=4)
    



## Limpieza de datos
with open('dat\covid_statistics.json') as file:
    datos = json.load(file)
df = pd.DataFrame(datos['response'])
df
    

data_list = df['cases'].tolist()
datos_casos = pd.DataFrame(data_list)
datos_casos = datos_casos[['new','active','critical','recovered','1M_pop','total']]
datos_casos.columns = ('new cases','active cases','critical','recovered','cases 1M_pop','total cases')
datos_casos


data_list2 = df['deaths'].tolist()
datos_muertes = pd.DataFrame(data_list2)
datos_muertes = datos_muertes[['new','1M_pop','total']]
datos_muertes.columns = ('new deaths','deaths 1M_pop','total deaths')
datos_muertes


data_list3 = df['tests'].tolist()
datos_tests = pd.DataFrame(data_list3)
datos_tests = datos_tests[['1M_pop','total']]
datos_tests.columns = ('tests 1M_pop','total tests')
datos_tests


covid = pd.concat([df, datos_casos, datos_muertes, datos_tests], axis=1)
covid


covid = covid.drop(['cases', 'deaths', 'tests','time','new cases','active cases','critical','cases 1M_pop',
                    'new deaths','deaths 1M_pop','tests 1M_pop','time'], axis=1)



## Filtramos por fecha
mask = (covid['day'] > '2022-12-31')
covid = covid.loc[mask]


print(covid['day'].unique())


##Eliminamos valores nulos
covid.isnull().sum()
covid.dropna(inplace= True)
covid



## Guardamos un nuevo fichero con el set de datos limpio:
covid.to_json(r'dat\Covid.json', orient = 'columns')




