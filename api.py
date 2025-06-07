import requests
from PIL import Image
from io import BytesIO
import re
from bd import Cachorro, DadosProcessados, Session

API_KEY = "live_lQAZAFRRtvwdlcc64vjw4je7BsrtfSquofW40NFCCPEgoNPNDofTZoq00sQestVd"

def mostrar_raca_por_id(raca_id, session):
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erro na API:", response.status_code)
        return

    dados = response.json()
    raca = next((r for r in dados if r['id'] == raca_id), None)
    if raca is None:
        print(f"Raça com id {raca_id} não encontrada.")
        return

    if 'image' in raca and 'url' in raca['image']:
        imagem_response = requests.get(raca['image']['url'])
        if imagem_response.status_code == 200:
            imagem = Image.open(BytesIO(imagem_response.content))
            imagem.show()

    if session.query(Cachorro).filter_by(id=raca_id).first() is None:
        novo = Cachorro(
            id=raca.get('id'), name=raca.get('name'), bred_for=raca.get('bred_for'),
            breed_group=raca.get('breed_group'), life_span=raca.get('life_span'),
            temperament=raca.get('temperament'), country_code=raca.get('country_code'),
            height_metric=raca.get('height', {}).get('metric'),
            weight_metric=raca.get('weight', {}).get('metric'),
            image_url=raca.get('image', {}).get('url')
        )
        session.add(novo)
        session.commit()
    processar_dados(raca_id, session)

def processar_dados(raca_id, session):
    cachorro = session.query(Cachorro).filter_by(id=raca_id).first()
    if not cachorro:
        return

    temperament_list = [t.strip() for t in (cachorro.temperament or '').split(',') if t.strip()]
    temperament_count = len(temperament_list)

    anos = re.findall(r'(\d+)', cachorro.life_span or '')
    min_life = int(anos[0]) if anos else None
    max_life = int(anos[1]) if len(anos) > 1 else min_life

    dados = session.query(DadosProcessados).filter_by(cachorro_id=raca_id).first()
    if not dados:
        dados = DadosProcessados(
            cachorro_id=raca_id,
            temperament_count=temperament_count,
            min_life_span=min_life,
            max_life_span=max_life
        )
        session.add(dados)
    else:
        dados.temperament_count = temperament_count
        dados.min_life_span = min_life
        dados.max_life_span = max_life
    session.commit()


def buscar_e_processar_racas():
    session = Session()
    for raca_id in range(1, 11):
        mostrar_raca_por_id(raca_id, session)
    session.close()