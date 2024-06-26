# -*- coding: utf-8 -*-
"""Ataque_Cardiaco.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bk8L_qzh_G9WAnTG0LzA0xSgBwpiUTMO

#análise de possibilidade de ataque cardíaco

## Descricao

idade - idade

sexo - sexo

dor - tipo de dor no peito (0 a 4)

press_arterial - pressão arterial em repouso

colesterol - colesterol sérico em mg/dl

glicose - glicemia de jejum > 120 mg/dl

eletrocardio - resultados do eletrocardiograma em repouso (valores 0, 1, 2)

freq_cardiaca - frequência cardíaca máxima alcançada

angina_ind - angina induzida por exercício

pico_ant = depressão do segmento ST induzida por exercício em relação ao repouso

declive - inclinação do segmento ST no pico do exercício

vasos_prin - número de vasos principais (0-3) coloridos por fluoroscopia

thalach - 0 = normal; 1 = defeito fixo; 2 = defeito reversível

var_alvo - target se tem menos chances 0 e mais chances 1

## Visualização dos Dados
"""

import pandas as pd

heart = pd.read_csv('heart.csv')
heart.head()

heart.tail()

heart.shape

heart.info()

heart.describe()

"""## Verificacao dos dados"""

heart.isnull().sum()

heart.duplicated().sum()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

idade = heart['age'].value_counts()
idade_heart = pd.DataFrame({'Age': idade.index, 'Count': idade.values})

plt.figure(figsize=(10, 6))
sns.lineplot(data=idade_heart, x='Age', y='Count')
plt.title('Contagem de Pacientes por Idade')
plt.xlabel('Idade')
plt.ylabel('Contagem')
plt.show()

heart.columns = ['idade', 'sexo', 'dor', 'press_arterial', 'colesterol', 'glicose', 'eletrocardio',
                 'freq_cardiaca', 'angina_ind', 'pico_ant', 'declive', 'vasos_prin', 'thalach', 'var_alvo']
heart.head()

"""1. Gráfico de Dispersão (Scatter Plot)
Para visualizar a relação entre duas variáveis quantitativas, como a pressão arterial e o colesterol, você pode usar um gráfico de dispersão.
"""

import seaborn as sns
import matplotlib.pyplot as plt


sns.scatterplot(data=heart, x='press_arterial', y='colesterol')
plt.show()

"""2. Visualização de um scatterplot da frequencia cardíaca com a pressão arterial."""

import matplotlib.pyplot as plt
sns.scatterplot(data=heart, x='press_arterial', y='freq_cardiaca')
plt.show()

"""3. Platagem em pares visualizando todos dos dados"""

import matplotlib.pyplot as plt
sns.pairplot(heart, hue='var_alvo')
plt.show()

"""4. Histograma
Para entender a distribuição de uma variável quantitativa, como a glicose, você pode usar um histograma.
"""

sns.histplot(data=heart, x='glicose', kde=True)
plt.show()

"""5. Displot dos atributos, visualizando 3 classes"""

import matplotlib.pyplot as plt
for col in heart.columns:
  sns.displot(x=col, data=heart, hue='var_alvo', bins=3)
  plt.show()

"""6. Gráfico de Violino
Para comparar a distribuição de uma variável quantitativa entre diferentes categorias, como a frequência cardíaca por sexo, você pode usar um gráfico de violino.
"""

sns.violinplot(data=heart, x='sexo', y='freq_cardiaca')
plt.show()

"""7. Gráfico de Correlação
Para visualizar a correlação entre todas as variáveis quantitativas, você pode usar um gráfico de correlação.
"""

correlacao = heart.corr()
sns.heatmap(correlacao, annot=True, cmap='coolwarm')

plt.figure(figsize=(20, 10))
plt.show()

"""8. Gráfico de Regressão
Para entender a relação entre duas variáveis quantitativas, como a idade e a pressão arterial, você pode usar um gráfico de regressão.
"""

sns.regplot(data=heart, x='idade', y='press_arterial')
plt.show()

"""9. Boxplot mostrando todos os outliers dos dados"""

import matplotlib.pyplot as plt

for col in heart.select_dtypes(include=['int64', 'float64']):
  plt.figure()
  plt.boxplot(heart[col])
  plt.title(f'Boxplot de {col}')
  plt.show()

"""10. Excluir todos o outliers indentificados"""

def remove_outliers(df, col):
  Q1 = df[col].quantile(0.25)
  Q3 = df[col].quantile(0.75)
  IQR = Q3 - Q1
  lower_bound = Q1 - 1.5 * IQR
  upper_bound = Q3 + 1.5 * IQR
  df_filtered = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
  return df_filtered

for col in heart.select_dtypes(include=['int64', 'float64']):
  heart = remove_outliers(heart, col)

heart.describe()

"""11. Boxplot das idades apos a remocao dos outliers"""

sns.boxplot(x=heart['idade'])

plt.title('Boxplot das idades')
plt.xlabel('Idades')
plt.ylabel('Valor')

plt.show()

"""## Visualização das Tabelas e Relações"""

plt.bar(heart['idade'].value_counts().index, heart['idade'].value_counts().values)
plt.xlabel('Idade')
plt.ylabel('Quantidade')
plt.title('Distribuição das idades')
plt.show()

#Classificação por idades

import matplotlib.pyplot as plt

plt.bar(heart['sexo'].value_counts().index, heart['sexo'].value_counts().values)
plt.xlabel('Sexo')
plt.ylabel('Quantidade')
plt.title('Distribuição do sexo')
plt.show()

#Quantidade por sexo

plt.bar(heart['dor'].value_counts().index, heart['dor'].value_counts().values)
plt.xlabel('Dor')
plt.ylabel('Quantidade')
plt.title('Distribuição da dor')
plt.show()

#Classificação da dor no peito

plt.bar(heart['eletrocardio'].value_counts().index, heart['eletrocardio'].value_counts().values)
plt.xlabel('Eletrocardio')
plt.ylabel('Quantidade')
plt.title('Distribuição do eletrocardiograma')
plt.show()

#resultados do eletrocardiograma de repouso

plt.bar(heart['pico_ant'].value_counts().index, heart['pico_ant'].value_counts().values)
plt.xlabel('Pico_ant')
plt.ylabel('Quantidade')
plt.title('Distribuição do picos anteriores')
plt.show()

#Mostra se as pessoas tiveram pico de ataque antes

plt.bar(heart['angina_ind'].value_counts().index, heart['angina_ind'].value_counts().values)
plt.xlabel('Angina_ind')
plt.ylabel('Quantidade')
plt.title('Distribuição da angina induzida')
plt.show()

#Nivel de angina induzida por exercício físicos

plt.bar(heart['vasos_prin'].value_counts().index, heart['vasos_prin'].value_counts().values)
plt.xlabel('Vasos_prin')
plt.ylabel('Quantidade')
plt.title('Distribuição dos vasos principais')
plt.show()

#Número de vasos principais coloridos por fluoroscopia

import matplotlib.pyplot as plt

declive = [0, 1, 2]
var_alvo = [0.5, 0.8, 0.9]

plt.plot(declive, var_alvo, marker='o', linestyle='-')

plt.xlabel('Declive')
plt.ylabel('Possibilidade de Ataque Cardíaco')
plt.title('Possibilidade de Ataque Cardíaco em relação ao Declive')

plt.grid(True)
plt.show()

plt.bar(heart['thalach'].value_counts().index, heart['thalach'].value_counts().values)
plt.xlabel('Thalach')
plt.ylabel('Quantidade')
plt.title('Distribuição da Taxa de Thalach')
plt.show()

#Taxa de Thalach é a maior freqüência cardíaca atingida durante o teste de esforço.

import matplotlib.pyplot as plt

labels = heart['dor'].value_counts().index.to_list()
sizes = heart['dor'].value_counts().to_list()

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
ax.set_title('Distribuição da dor no peito')
plt.show()

#Distribuicao de dados relatados a dor

heart.groupby(['sexo','dor']).size().unstack()

heart.groupby(['var_alvo', 'declive']).size().unstack()

"""##Tratamento dos dados para o treinamento

"""



heart.duplicated().sum()

# prompt: mostre as duplicadas na tabela

heart[heart.duplicated()]

from sklearn.preprocessing import MinMaxScaler

normalizacao = MinMaxScaler()
heart_normalizacao = normalizacao.fit_transform(heart)

heart_normalizacao = pd.DataFrame(heart_normalizacao, columns=heart.columns)

heart_normalizacao.head()

heart_normalizacao.tail()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

X = heart_normalizacao.drop('var_alvo', axis=1)
y = heart_normalizacao['var_alvo']
modelo_regressao_logistica = LogisticRegression()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scores = cross_val_score(modelo_regressao_logistica, X, y, cv=10)

modelo_regressao_logistica.fit(X_train, y_train)
score_medio = scores.mean()

y_previsto = modelo_regressao_logistica.predict(X_test)

acuracia = accuracy_score(y_test, y_previsto)
print("Acurácia Regressao Logistica:", acuracia * 100, "%")
print("Score médio da regressao logistica:", score_medio * 100, '%')

from sklearn.ensemble import RandomForestClassifier

modelo_random_forest = RandomForestClassifier(n_estimators=5)
modelo_random_forest.fit(X_train, y_train)

y_previsto_random_forest = modelo_random_forest.predict(X_test)
acuracia_media_random_forest = accuracy_score(y_test, y_previsto_random_forest)
score_media_random_forest = modelo_random_forest.score(X_test, y_test)

acuracia_random_forest = accuracy_score(y_test, y_previsto_random_forest)
print("Acurácia Random Forest:", acuracia_random_forest * 100, "%")
print("Acurácia média Random Forest:", score_media_random_forest * 100, '%')

from sklearn.neural_network import MLPClassifier

modelo_rede_neural = MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', max_iter=1000)
modelo_rede_neural.fit(X_train, y_train)

y_previsto_rede_neural = modelo_rede_neural.predict(X_test)
acuracia_rede_neural = accuracy_score(y_test, y_previsto_rede_neural)
score_medio_rede_neural = modelo_rede_neural.score(X_test, y_test)

print("Acurácia Rede Neural: {:.2f}%".format(acuracia_rede_neural * 100))
print("Score médio da rede neural: {:.2f}%".format(score_medio_rede_neural * 100))