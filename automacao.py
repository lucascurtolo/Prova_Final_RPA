from bd import Session, Cachorro, DadosProcessados
from api import buscar_e_processar_racas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

CHAVE = b"ekOdnW1rX-_5L3_zCYQUcBEaIlxcNigEh0ElsKWBzfk="
SENHA_CRIPTOGRAFADA = b"gAAAAABoQgtb7SVSVnuypo70fpphyVuL7RZNUIXYD_x311GBBPWTUdNy63FEbKCOSLa5KsQ96bvDvShSnK9UugdCLJIn-GiQHkUNTB_KOfNQiCO_KEkRsVg="
EMAIL_REMETENTE = "lucascurtolobelem@gmail.com"
EMAIL_DESTINATARIO = "lucasc.belem@gmail.com"

def obter_senha():
    fernet = Fernet(CHAVE)
    return fernet.decrypt(SENHA_CRIPTOGRAFADA).decode()

def gerar_relatorio():
    session = Session()
    relatorio = "Relatório de Raças de Cães Processadas\n\n"
    dados = session.query(Cachorro).join(DadosProcessados).all()
    for cachorro in dados:
        dp = cachorro.dados_processados
        relatorio += (
            f"Raça: {cachorro.name}\nTemperamentos: {cachorro.temperament}\n"
            f"Número de temperamentos: {dp.temperament_count}\n"
            f"Vida útil: {cachorro.life_span} (Min: {dp.min_life_span}, Max: {dp.max_life_span})\n"
            "-----------------------------\n"
        )
    session.close()
    return relatorio

def enviar_email(corpo):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = "Relatório Automático - Raças de Cães"
    msg.attach(MIMEText(corpo, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, obter_senha())
        server.send_message(msg)
    print("E-mail enviado com sucesso!")

if __name__ == "__main__":
    buscar_e_processar_racas()
    corpo = gerar_relatorio()
    enviar_email(corpo)
