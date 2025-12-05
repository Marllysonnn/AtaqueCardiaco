from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import traceback

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    modelo_path = os.path.join(BASE_DIR, 'Treinamento', 'data', 'heart_model.pkl')
    with open(modelo_path, 'rb') as f:
        modelo = pickle.load(f)
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print(traceback.format_exc())
    modelo = None

heart_normalizacao_path = os.path.join(BASE_DIR, 'Treinamento', 'data', 'base_normalizada.csv')
heart_data_path = os.path.join(BASE_DIR, 'Treinamento', 'data', 'heart.csv')

heart_normalizacao = pd.read_csv(heart_normalizacao_path)
heart_data = pd.read_csv(heart_data_path)

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
    
    dados = request.json  # Use request.json diretamente para obter os dados JSON
    
    try:
        # Adicione mensagens de depuração para verificar os dados recebidos
        print("Dados recebidos:", dados)


        idade = dados['idade']
        sexo = dados['sexo']
        tipo_dor_toracica = dados['tipo_dor_toracica']
        pressao_arterial = dados['pressao_arterial']
        colesterol = dados['colesterol']
        acucar_sanguineo = dados['acucar_sanguineo']
        resultados_eletrocardiograficos = dados['resultados_eletrocardiograficos']

        dados_de_entrada = [[
            idade, sexo, tipo_dor_toracica, pressao_arterial, colesterol,
            acucar_sanguineo, resultados_eletrocardiograficos,
        ]]
        
        previsao = modelo.predict(dados_de_entrada)

        # Adicione mensagens de depuração para verificar a previsão
        print("Previsão:", previsao)

        return jsonify({'previsao': int(previsao[0])})
    except Exception as e:
        # Adicione mensagens de depuração para verificar qualquer erro
        print("Erro ao processar a previsão:", e)

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
        total_records = len(heart_normalizacao)
        dor_tipo_2_count = len(heart_normalizacao[heart_normalizacao['dor'] == 1.0])
        diabetes_count = len(heart_normalizacao[heart_normalizacao['eletrocardio'] == 0.5])
        ambos_count = len(heart_normalizacao[(heart_normalizacao['dor'] == 1.0) & (heart_normalizacao['eletrocardio'] == 0.5)])

        dor_tipo_2_percentage = (dor_tipo_2_count / total_records) * 100
        diabetes_percentage = (diabetes_count / total_records) * 100
        ambos_percentage = (ambos_count / total_records) * 100

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

@app.route('/')
def home():
    return render_template('index.html')
