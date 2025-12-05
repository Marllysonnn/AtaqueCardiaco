from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import traceback
import os
from flask_cors import CORS
CORS(app)


app = Flask(__name__)
    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==== CARREGAMENTO DO MODELO ====
try:
    modelo_path = os.path.join(BASE_DIR, 'Treinamento', 'data', 'heart_model.pkl')
    with open(modelo_path, 'rb') as f:
        modelo = pickle.load(f)
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print(traceback.format_exc())
    modelo = None

# ==== BASES ====
heart_normalizacao_path = os.path.join(BASE_DIR, 'Treinamento', 'data', 'base_normalizada.csv')
heart_data_path = os.path.join(BASE_DIR, 'Treinamento', 'data', 'heart.csv')

heart_normalizacao = pd.read_csv(heart_normalizacao_path)
heart_data = pd.read_csv(heart_data_path)

# ==== ROTAS ====

@app.route('/dados_ataque_cardiaco', methods=['GET'])
def dados_ataque_cardiaco():
    ataque = heart_data[heart_data['target'] == 1]
    return jsonify({
        'Homem': int(ataque[ataque['sex'] == 1].shape[0]),
        'Mulher': int(ataque[ataque['sex'] == 0].shape[0])
    })

@app.route('/prever', methods=['POST'])
def prever():
    if modelo is None:
        return jsonify({'erro': 'Modelo não carregado'}), 500

    try:
        dados = request.json

        entrada = [[
            dados['idade'],
            dados['sexo'],
            dados['tipo_dor_toracica'],
            dados['pressao_arterial'],
            dados['colesterol'],
            dados['acucar_sanguineo'],
            dados['resultados_eletrocardiograficos']
        ]]

        previsao = modelo.predict(entrada)

        return jsonify({'previsao': int(previsao[0])})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'erro': str(e)}), 500

@app.route('/heart')
def heart():
    return jsonify(heart_normalizacao.to_dict(orient='records'))

@app.route('/dados_histograma')
def dados_histograma():
    faixas = {
        "80+": (80, 100),
        "74-79": (74, 79),
        "68-73": (68, 73),
        "62-67": (62, 67),
        "56-61": (56, 61),
        "50-55": (50, 55)
    }

    data = []

    for faixa, (min_age, max_age) in faixas.items():
        data.append({
            'age': faixa,
            'homens_ataque': int(heart_data[(heart_data['sex'] == 1) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 1)].shape[0]),
            'mulheres_ataque': int(heart_data[(heart_data['sex'] == 0) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 1)].shape[0]),
            'homens_sem': int(heart_data[(heart_data['sex'] == 1) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 0)].shape[0]),
            'mulheres_sem': int(heart_data[(heart_data['sex'] == 0) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 0)].shape[0])
        })

    return jsonify(data)

@app.route('/dados_venn')
def dados_venn():
    total = len(heart_normalizacao)

    dor = len(heart_normalizacao[heart_normalizacao['dor'] == 1.0])
    diabetes = len(heart_normalizacao[heart_normalizacao['eletrocardio'] == 0.5])
    ambos = len(heart_normalizacao[(heart_normalizacao['dor'] == 1.0) & (heart_normalizacao['eletrocardio'] == 0.5)])

    return jsonify([
        {"name": "Dor Tipo 2", "value": (dor / total) * 100},
        {"name": "Diabetes", "value": (diabetes / total) * 100},
        {"name": "Ambos", "value": (ambos / total) * 100}
    ])

# ==== PORTA AUTOMÁTICA DO RENDER ====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
