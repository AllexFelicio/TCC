# -*- coding: utf-8 -*-
"""PrototipoTCC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S5agkJkC5gtDik7P0mcau6h6vgMRCfqp
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree
from sklearn.model_selection import GridSearchCV

dados = pd.read_csv('Breast_cancer_data.csv')
dados.head()

dados.info()

sns.countplot(x='diagnosis', data = dados)
plt.show()
dados['diagnosis'].value_counts()

# Criando o pairplot com tamanho ajustado
sns.pairplot(dados.iloc[:,1:6], hue="diagnosis", height=2)

# Exibindo o gráfico
plt.show()

plt.figure(figsize=(15,7))
sns.heatmap(dados.corr())
ax = sns.heatmap(dados.corr(),vmin=-1,vmax=1,center=0,annot=True)
plt.show()

X = dados.drop(columns={'diagnosis'}, axis=1)
y = dados['diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y,  random_state = 1)
print(X.shape, X_train.shape, X_test.shape)
print(y.shape, y_train.shape, y_test.shape)

#Normalizando os dados
scaler = StandardScaler()
X_train_normalizado = scaler.fit_transform(X_train)
X_test_normalizado = scaler.transform(X_test)

print(X_train_normalizado)

from sklearn.metrics import confusion_matrix
# Aplicação do KNN
knn = KNeighborsClassifier(n_neighbors=28)
knn.fit(X_train_normalizado, y_train)
knn_predictions = knn.predict(X_test_normalizado)
knn_accuracy = accuracy_score(y_test, knn_predictions)

cm = confusion_matrix(y_test, knn_predictions)
print(cm)

#Aplicação do Floresta Aleatória
rf = RandomForestClassifier(n_estimators=50,random_state=42,max_depth=50)
rf.fit(X_train_normalizado, y_train)
rf_predictions = rf.predict(X_test_normalizado)
rf_accuracy = accuracy_score(y_test, rf_predictions)

#pega a primeira árvore da floresta
#estimator = rf.estimators_[0]
#plt.figure(figsize=(20,15))
#plot_tree(estimator, filled=True, rounded=True, class_names=['0', '1'], feature_names=['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness'], max_depth=3)
#plt.show()

# Aplicação do Naive Bayes
nb = GaussianNB()
nb.fit(X_train_normalizado, y_train)
nb_predictions = nb.predict(X_test_normalizado)
nb_accuracy = accuracy_score(y_test, nb_predictions)

# Gráfico
labels = ['KNN', 'Floresta Aleatória', 'Naive Bayes']
accuracies = [knn_accuracy, rf_accuracy, nb_accuracy]

plt.bar(labels, accuracies, color=['lightblue', 'lightgreen', 'lightcoral'])

for i in range(len(labels)):
    plt.text(i, accuracies[i], f'{accuracies[i]*100:.2f}%', ha = 'center', va='bottom')

plt.ylabel('Acurácia')
plt.title('Comparação de Desempenho dos Modelos')
plt.show()

# Para o KNN:
knn = KNeighborsClassifier()
knn_grid = {'n_neighbors': list(range(1, 31))}
knn_cv = GridSearchCV(knn, knn_grid, cv=5)
knn_cv.fit(X_train_normalizado, y_train)
knn_best_params = knn_cv.best_params_
knn_best_score = knn_cv.best_score_

plt.figure(figsize=(10, 6))
plt.plot(knn_cv.cv_results_['param_n_neighbors'].data, knn_cv.cv_results_['mean_test_score'], marker='o')
plt.title('Acurácia da validação cruzada vs número de vizinhos')
plt.xlabel('Número de vizinhos')
plt.ylabel('Acurácia da validação cruzada')
plt.grid()
plt.show()

# Para a Floresta Aleatória:
rf = RandomForestClassifier()
rf_grid = {'n_estimators': [50, 100, 150, 200, 250], 'max_depth': [None, 10, 20, 30, 40, 50]}
rf_cv = GridSearchCV(rf, rf_grid, cv=5)
rf_cv.fit(X_train_normalizado, y_train)
rf_best_params = rf_cv.best_params_
rf_best_score = rf_cv.best_score_

results = pd.DataFrame(rf_cv.cv_results_)

# Extrair as colunas relevantes
scores = results[['param_n_estimators', 'param_max_depth', 'mean_test_score']]

# Pivotar a tabela para que tenhamos n_estimators ao longo do eixo x, max_depth ao longo do eixo y, e a acurácia média como valores
scores = scores.pivot_table(index='param_max_depth', columns='param_n_estimators', values='mean_test_score')

# Configurar tamanho da figura
plt.figure(figsize=(10, 6))

# Plotar a curva de validação cruzada
for depth, score in scores.items():
    plt.plot(scores.columns, score, marker='o', label=f"max_depth={depth}")

# Configura título, rótulos dos eixos e legenda
plt.title('Acurácia da validação cruzada para diferentes hiperparâmetros')
plt.xlabel('Número de estimadores')
plt.ylabel('Acurácia da validação cruzada')
plt.legend(title='max_depth')

# Configurar grade
plt.grid()

# Mostrar o gráfico
plt.show()