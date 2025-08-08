# 🐶 Prova Final RPA - API de Raças de Cachorros

Este projeto é uma automação Python desenvolvida como parte de uma avaliação de RPA (Automação de Processos Robóticos). Ele consome dados da [The Dog API](https://thedogapi.com/), processa informações relevantes sobre raças de cães e armazena em um banco de dados local usando SQLAlchemy.

---

## 🚀 Funcionalidades

- Acessa a API do The Dog API usando uma chave de autenticação.
- Busca informações detalhadas de raças por ID.
- Mostra a imagem da raça usando `PIL`.
- Armazena dados das raças em um banco de dados local (nome, grupo, expectativa de vida, peso, altura, temperamento, etc).
- Processa o número de temperamentos e expectativa de vida mínima e máxima.
- Automatiza a consulta para múltiplas raças (IDs de 1 a 10).

---

## 🛠 Tecnologias utilizadas

- Python 3.11+
- [requests](https://pypi.org/project/requests/)
- [Pillow (PIL)](https://pypi.org/project/Pillow/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- API: [The Dog API](https://thedogapi.com/)

---

## 📁 Estrutura do Projeto

