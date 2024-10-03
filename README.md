# facebook-expertsender-api

# Objetivo
- Receber dados dos forms do facebook e enviar para a ExpertSender

# Como rodar:
- Instalar as dependencias:
    $ pip install -r requirements.txt

- Start no servidor:
    $ gunicorn app:app

# Rotas:
- POST: /webhook/facebook-leads
Body:
{
    "email": "usuario@email.com",
    "first_name": "Usuario",
    "last_name": "de Teste"
}

- GET: /webhook/facebook-leads
Parametros: 
    ?hub.verify_token={{token}}
    &hub.challenge={{challenge}}

- GET: /test
Irá retornar uma messagem caso a api esteja rodando e funcionando