import random
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import traceback

app = Flask(__name__)

try:
    with open('Treinamento/data/modelo_treinado.pkl', 'rb') as f:
        modelo = pickle.load(f)
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print(traceback.format_exc())
    modelo = None

heart_normalizacao = pd.read_csv('Treinamento/data/base_normalizada.csv')
heart_data = pd.read_csv('Treinamento/data/heart.csv')

@app.route('/dados_ataque_cardiaco', methods=['GET'])
def dados_ataque_cardiaco():
    ataque_cardiaco = heart_data[heart_data['target'] == 1]
    
    homens = ataque_cardiaco[ataque_cardiaco['sex'] == 1].shape[0]
    mulheres = ataque_cardiaco[ataque_cardiaco['sex'] == 0].shape[0]
    
    return jsonify({'Homem': homens, 'Mulher': mulheres})

@app.route('/prever', methods=['POST'])
def prever():
    if modelo is None:
        return jsonify({'erro': 'Modelo não está disponível'}), 500
    
    dados = request.get_json(force=True)
    
    try:
        idade = dados['idade']
        sexo = dados['sexo']
        pressao_arterial = dados['pressao_arterial']
        colesterol = dados['colesterol']
        resultados_eletrocardiograficos = dados['resultados_eletrocardiograficos']
        acucar_sanguineo = dados['acucar_sanguineo']
        tipo_dor_toracica = dados['tipo_dor_toracica']
        
        frequencia_cardiaca_maxima = random.randint(80, 200)
        angina_exercicio = random.choice([0, 1])
        depressao_exercicio = round(random.uniform(0.0, 4.0), 1)
        inclincao_ST = random.choice([0, 1, 2])
        numero_vasos_coloridos = random.choice([0, 1, 2])
        thal = random.choice([0, 1, 2, 3])

        dados_de_entrada = [[
            idade, sexo, tipo_dor_toracica, pressao_arterial, colesterol,
            acucar_sanguineo, resultados_eletrocardiograficos, frequencia_cardiaca_maxima,
            angina_exercicio, depressao_exercicio, inclincao_ST, numero_vasos_coloridos, thal
        ]]
        
        previsao = modelo.predict(dados_de_entrada)
        return jsonify({'previsao': int(previsao[0])})
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar a previsão: {e}'}), 500

@app.route('/heart', methods=['GET'])
def heart():
    try:
        data = heart_normalizacao.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar os dados: {e}'}), 500

@app.route('/dados_histograma', methods=['GET'])
def dados_histograma():
    try:
        faixas_etarias = {
            "80+": (80, 100),
            "74-79": (74, 79),
            "68-73": (68, 73),
            "62-67": (62, 67),
            "56-61": (56, 61),
            "50-55": (50, 55)
        }

        data = []
        for faixa, (min_age, max_age) in faixas_etarias.items():
            homens_ataque = heart_data[(heart_data['sex'] == 1) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 1)].shape[0]
            mulheres_ataque = heart_data[(heart_data['sex'] == 0) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 1)].shape[0]
            homens_sem_ataque = heart_data[(heart_data['sex'] == 1) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 0)].shape[0]
            mulheres_sem_ataque = heart_data[(heart_data['sex'] == 0) & (heart_data['age'] >= min_age) & (heart_data['age'] <= max_age) & (heart_data['target'] == 0)].shape[0]

            data.append({
                'age': faixa,
                'homens_ataque': homens_ataque,
                'mulheres_ataque': mulheres_ataque,
                'homens_sem_ataque': homens_sem_ataque,
                'mulheres_sem_ataque': mulheres_sem_ataque
            })

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dados_venn', methods=['GET'])
def dados_venn():
    try:
        # Calculating the percentage of each condition
        total_records = len(heart_normalizacao)
        dor_tipo_2_count = len(heart_normalizacao[heart_normalizacao['dor'] == 1.0])
        diabetes_count = len(heart_normalizacao[heart_normalizacao['eletrocardio'] == 0.5])
        ambos_count = len(heart_normalizacao[(heart_normalizacao['dor'] == 1.0) & (heart_normalizacao['eletrocardio'] == 0.5)])

        # Calculate the percentage of each condition
        dor_tipo_2_percentage = (dor_tipo_2_count / total_records) * 100
        diabetes_percentage = (diabetes_count / total_records) * 100
        ambos_percentage = (ambos_count / total_records) * 100

        # Return data in JSON format
        data = [
            {"name": "Dor Tipo 2", "value": dor_tipo_2_percentage},
            {"name": "Diabetes", "value": diabetes_percentage},
            {"name": "Ambos", "value": ambos_percentage}
        ]

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
