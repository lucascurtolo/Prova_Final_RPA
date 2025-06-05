import requests
from PIL import Image
from io import BytesIO
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Cachorro(Base):
    __tablename__ = "cachorros"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bred_for = Column(String)
    breed_group = Column(String)
    life_span = Column(String)
    temperament = Column(String)
    country_code = Column(String)
    height_metric = Column(String)
    weight_metric = Column(String)
    image_url = Column(String)


engine = create_engine("sqlite:///projeto_rpa.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


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
    print(f"country_code: {raca.get('country_code', 'N/A')}")
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

    session = Session()
    if session.query(Cachorro).filter_by(id=raca_id).first() is None:
        novo_cachorro = Cachorro(
            id=raca.get('id'),
            name=raca.get('name'),
            bred_for=raca.get('bred_for'),
            breed_group=raca.get('breed_group'),
            life_span=raca.get('life_span'),
            temperament=raca.get('temperament'),
            country_code=raca.get('country_code'),
            height_metric=raca.get('height', {}).get('metric'),
            weight_metric=raca.get('weight', {}).get('metric'),
            image_url=raca.get('image', {}).get('url')
        )
        session.add(novo_cachorro)
        session.commit()
        print("Raça salva no banco de dados.")
    else:
        print("Raça já existe no banco de dados.")
    session.close()


mostrar_raca_por_id(5)
