import requests
from PIL import Image
from io import BytesIO
import re
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

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

    dados_processados = relationship(
        "DadosProcessados", back_populates="cachorro", uselist=False)


class DadosProcessados(Base):
    __tablename__ = "dados_processados"

    id = Column(Integer, primary_key=True)
    cachorro_id = Column(Integer, ForeignKey("cachorros.id"))
    temperament_count = Column(Integer)
    min_life_span = Column(Integer)
    max_life_span = Column(Integer)

    cachorro = relationship("Cachorro", back_populates="dados_processados")

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
    processar_dados(raca_id, session)
    session.close()

def processar_dados(raca_id, session):
    cachorro = session.query(Cachorro).filter_by(id=raca_id).first()
    if not cachorro:
        print("Raça não encontrada no banco para processar.")
        return

    # Contar temperamentos
    temperament = cachorro.temperament or ""
    temperament_list = [t.strip() for t in temperament.split(",") if t.strip()]
    temperament_count = len(temperament_list)

    # Extrair min e max life span com regex
    life_span = cachorro.life_span or ""
    anos = re.findall(r'(\d+)', life_span)
    min_life_span = int(anos[0]) if anos else None
    max_life_span = int(anos[1]) if len(anos) > 1 else min_life_span

    dados_existentes = session.query(
        DadosProcessados).filter_by(cachorro_id=raca_id).first()

    if dados_existentes is None:
        dados_processados = DadosProcessados(
            cachorro_id=raca_id,
            temperament_count=temperament_count,
            min_life_span=min_life_span,
            max_life_span=max_life_span
        )
        session.add(dados_processados)
    else:
        dados_existentes.temperament_count = temperament_count
        dados_existentes.min_life_span = min_life_span
        dados_existentes.max_life_span = max_life_span

    session.commit()
    print(f"Dados processados para a raça {cachorro.name} foram salvos.")


def gerar_relatorio():
    session = Session()
    relatorio = "Relatório de Raças de Cães Processadas\n\n"
    dados = session.query(Cachorro).join(DadosProcessados).all()
    if not dados:
        session.close()
        return "Nenhum dado processado encontrado."
    for cachorro in dados:
        dp = cachorro.dados_processados
        relatorio += (
            f"Raça: {cachorro.name}\n"
            f"Temperamentos: {cachorro.temperament}\n"
            f"Número de temperamentos: {dp.temperament_count}\n"
            f"Vida útil: {cachorro.life_span} (Min: {dp.min_life_span}, Max: {dp.max_life_span})\n"
            "-----------------------------\n"
        )
    session.close()
    return relatorio


chave = b"ekOdnW1rX-_5L3_zCYQUcBEaIlxcNigEh0ElsKWBzfk="
senha_criptografada = b"gAAAAABoQgtb7SVSVnuypo70fpphyVuL7RZNUIXYD_x311GBBPWTUdNy63FEbKCOSLa5KsQ96bvDvShSnK9UugdCLJIn-GiQHkUNTB_KOfNQiCO_KEkRsVg="


def obter_senha():
    fernet = Fernet(chave)
    return fernet.decrypt(senha_criptografada).decode()


def enviar_email(corpo):
    remetente = "lucascurtolobelem@gmail.com"
    destinatario = "lucasc.belem@gmail.com"
    senha = obter_senha()

    assunto = "Relatório Automático - Raças de Cães"

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    servidor_smtp = "smtp.gmail.com"
    porta_smtp = 587

    with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
    print("E-mail enviado com sucesso!")


if __name__ == "__main__":
    # Buscar e salvar/processar raças com IDs de 1 a 10
    for raca_id in range(1, 11):
        mostrar_raca_por_id(raca_id)

    # Gerar o relatório
    corpo_email = gerar_relatorio()

    # Enviar o e-mail com o relatório
    enviar_email(corpo_email)
