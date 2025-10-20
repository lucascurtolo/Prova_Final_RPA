🚀 Visão Geral

Este projeto tem como objetivo automatizar o processo de coleta, análise e envio de dados de raças de cães com os seguintes passos principais:

Consumir a API externa para obter dados sobre raças.

Processar e transformar os dados (limpeza, agregação, armazenamento).

Gerar relatório com os resultados.

Enviar o relatório automaticamente por e-mail.

🧰 Estrutura do Projeto

api.py – módulo responsável por consultar a API de raças de cães.

bd.py – módulo para manipulação de banco de dados ou armazenamento local dos dados coletados.

automacao.py – módulo principal que orquestra o fluxo (coleta → processamento → relatório → envio).

requirements.txt – lista de dependências Python necessárias para execução.

Relatório_de_RPA_Prova_Final.pdf – documento descritivo com detalhes do projeto (opcional).

📦 Tecnologias e Dependências

Python (versão recomendada ≥ 3.x)

Principais bibliotecas: requests, pandas, etc. (veja requirements.txt)

Qualquer sistema de banco de dados compatível ou armazenamento local leve.

Configuração de e-mail (SMTP) para envio automático.

✅ Resultados Esperados

Dados atualizados das raças de cães obtidos da API.

Armazenamento local ou em banco dos dados processados.

Relatório contendo os insights principais (ex: contagem por tipo, média de atributos).

Envio automático do relatório por e-mail para o(s) destinatário(s) configurado(s).

