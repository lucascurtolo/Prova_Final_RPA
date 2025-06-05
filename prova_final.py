import requests
from PIL import Image
from io import BytesIO


def mostrar_raca_por_id(raca_id):
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {
        "x-api-key": "live_lQAZAFRRtvwdlcc64vjw4je7BsrtfSquofW40NFCCPEgoNPNDofTZoq00sQestVd"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erro na API:", response.status_code)
        return

    dados = response.json()

  
    raca = next((r for r in dados if r['id'] == raca_id), None)

    if raca is None:
        print(f"Raça com id {raca_id} não encontrada.")
        return

    
    print(f"Nome: {raca.get('name', 'N/A')}")
    print(f"Bred for: {raca.get('bred_for', 'N/A')}")
    print(f"Breed group: {raca.get('breed_group', 'N/A')}")
    print(f"Life span: {raca.get('life_span', 'N/A')}")
    print(f"Temperament: {raca.get('temperament', 'N/A')}")
    print(f"Origin: {raca.get('origin', 'N/A')}")
    print(f"Height (cm): {raca.get('height', {}).get('metric', 'N/A')}")
    print(f"Weight (kg): {raca.get('weight', {}).get('metric', 'N/A')}")

    
    if 'image' in raca and 'url' in raca['image']:
        imagem_url = raca['image']['url']
        print("Mostrando imagem...")
        imagem_response = requests.get(imagem_url)
        if imagem_response.status_code == 200:
            imagem = Image.open(BytesIO(imagem_response.content))
            imagem.show()
        else:
            print("Erro ao baixar a imagem.")
    else:
        print("Imagem não disponível para esta raça.")

mostrar_raca_por_id(10)
