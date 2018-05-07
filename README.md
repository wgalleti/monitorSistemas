# Monitoramento de rotinas importantes dos Sistemas

* ERP (Logs de processo automático)

## Configuração

| Atributo | Descrição | Exemplo |
| --- | --- | --- |
|DB_HOST | Endereço do banco | 192.168.0.10 ou banco.seudominio.com |
|DB_PORT | Porta do banco | 1521 |
|DB_USER | Usuário do banco | usuario |
|DB_PASS | Senha do Banco | senha |
|DB_SERVICE | Service Name do Banco | PROD ou QA |
|EMAIL_USER | Endereço de Email office365 | email@seudominio.com |
|EMAIL_PASS | Senha do Email | suasenha |
|EMAIL_TO | Endereço de destino | para@seudominio.com.br |

```
DB_HOST=banco.seudominio.com
DB_PORT=1521
DB_USER=usuario
DB_PASS=senha
DB_SERVICE=PROD
EMAIL_USER=email@seudominio.com
EMAIL_PASS=suasenha
EMAIL_TO=para@seudominio.com.br
``` 

## Instalação e utilização

Requer python 3.6 e pipenv

* Crie o ambiente virtual `python -m venv .venv`
* Ative o ambiente virtual
    * Windows `.venv\Scripts\activate`
    * Linux ou Mac `source .venv\bin\activate`
* Instale as dependências `pipenv install`
* Crie o arquivo de configuração `.env` ([Exemplo](#configuracao))
* Rode a aplicação `python src/processo_automatico.py`
