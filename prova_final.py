import requests
import pprint


url = "https://api.thedogapi.com/v1/breeds"

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    pprint.pprint(dados[1])
else:
    print("Erro ao acessar a APi:", response.status_code)
