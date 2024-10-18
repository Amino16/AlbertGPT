
from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()  # Charge les variables depuis le fichier .env

openai.api_key = os.getenv('OPENAI_API_KEY')

# Fonction pour lire le fichier .txt contenant les informations importantes
def get_school_info():
    try:
        with open('school_info.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        return "Erreur lors de la lecture du fichier texte."

# Fonction pour interagir avec GPT via l'API OpenAI
def chat_with_gpt(prompt, school_info):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Vous êtes un assistant scolaire. Ne parlez que de scolarité et d'orientation. Ignorez tout sujet inapproprié comme la violence, les armes, les soirées, etc. Voici des informations sur l'école : {school_info}."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Erreur: {str(e)}"

# Route pour l'accueil (GET)
@app.route('/')
def home():
    return render_template('index.html')

# Route pour traiter les requêtes POST pour le chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Aucun prompt fourni"}), 400

    # Lecture des informations de l'école depuis le fichier texte
    school_info = get_school_info()

    response = chat_with_gpt(prompt, school_info)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
