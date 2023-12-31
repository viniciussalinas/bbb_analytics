# -*- coding: utf-8 -*-
"""bbb-analytics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QO-fLI3M2aT5HqNtuPV_SEeGDYoK9pPv
"""

# Importando bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np

# Lendo dataset
df = pd.read_excel('dataset_bbb.xlsx', index_col=None)

# Exibindo os 6 primeiros registros
df.head(6)

# Renomeando colunas para maior facilidade em comandos
df = df.rename(columns={"Edição": "edicao", "Ano de edição": "ano_edicao", "Nome Completo": "nome", "Data de Nascimento": "data_nascimento", "Gênero": "genero", "Cor": "cor", "Idade": "idade", "LGBTQIA+": "lgbtqia", "Profissão": "profissao", "Categoria Profissional": "cat_profissional", "Camarote": "camarote", "Cidade de nascimento": "cidade_nasc", "Estado de nascimento": "estado_nasc", "Região de nascimento": "regiao_nasc", "Colocação": "colocacao", "Posição": "posicao", "Meio de indicação": "indicacao", "Eliminação (%)": "eliminacao", "Finalista (%)": "final", "Rejeição (%)": "rejeicao"})

# Criação de uma nova coluna: finalista
def ff(df):
    if df['indicacao'] == 'Finalista':
        val = 1
    else:
        val = 0
    return val

df['finalista'] = df.apply(ff, axis=1)

# Criação de uma nova coluna: vencedor
def fv(df):
    if df['colocacao'] == 'Vencedor':
        val = 1
    else:
        val = 0
    return val

df['vencedor'] = df.apply(fv, axis=1)

# Criação de uma nova coluna: ultimas_edicoes, em que 1 evidencia participantes da edição 11 a 21
def fu(df):
    if df['edicao'] > 10:
        val = 1
    else:
        val = 0
    return val

df['ultimas_edicoes'] = df.apply(fu, axis=1)

# Verificação das alterações e acréscimos
df.head()

# Análise de variáveis que contém registros vazios
df.isnull().any()

# Análise do tipo de cada variável
df.dtypes

# Visualização da quantidade de linhas e colunas do dataset
df.shape

# Resumo estatítico de variáveis quantitativas
df.describe()

# Instalação de um módulo a ser utilizado
!pip install sweetviz

import sweetviz as sv

my_report = sv.analyze(df)
my_report.show_html()

dfs = df.drop(columns=['data_nascimento'])

my_report2 = sv.compare_intra(dfs, dfs["edicao"] < 11,["Primeiras Edicoes", "Ultimas Edicoes"])
my_report2.show_html()

c = df['indicacao'].value_counts()
p = df['indicacao'].value_counts(normalize=True)
pd.concat([c,p], axis=1, keys=['Contagem', '%'])

sns.distplot(df['idade'])

# Análise de diversidade de cor dentre as 21 edições do programa
df.groupby(['edicao','cor']).size().groupby(level=0).apply(
    lambda x: 100 * x / x.sum()
).unstack().plot(kind='bar',figsize=(16,8),stacked=True)

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.show()

# Análise de profissões dentre as 21 edições do programa
df.groupby(['edicao','cat_profissional']).size().groupby(level=0).apply(
    lambda x: 100 * x / x.sum()
).unstack().plot(kind='bar',figsize=(16,8),stacked=True)

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.show()

# Análise de regiões dentre as 21 edições do programa
df.groupby(['edicao','regiao_nasc']).size().groupby(level=0).apply(
    lambda x: 100 * x / x.sum()
).unstack().plot(kind='bar',figsize=(16,8),stacked=True)

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.show()

fig = plt.figure(figsize=(20,8))

sns.boxplot(x='edicao',y='idade',data=df,color='cyan')

sns.distplot(df['eliminacao'])

sns.distplot(df['final'])

grouped_multiple = df.groupby(['genero', 'ultimas_edicoes']).agg({'finalista': ['mean', 'sum', 'count']})
grouped_multiple.columns = ['percentual', 'finalistas', 'total']
grouped_multiple = grouped_multiple.reset_index()
print(grouped_multiple)

primeiras = [16.2,17.5]
ultimas = [21.8,9.5]

x1 =  np.arange(len(primeiras))
x2 = [x + 0.15 for x in x1]

# Plota as barras
plt.bar(x1, primeiras, width=0.15, label = '10 Primeiras Edições', color = 'gray')
plt.bar(x2, ultimas, width=0.15, label = '11 Últimas Edições', color = 'brown')

genero = ['Feminino','Masculino']
plt.xticks([x for x in range(len(primeiras))], genero)

# inseri uma legenda no gráfico
plt.legend()

plt.title("Percentual de Participantes Finalistas")
plt.show()

grouped_multiple = df.groupby(['genero', 'ultimas_edicoes']).agg({'vencedor': ['mean', 'sum', 'count']})
grouped_multiple.columns = ['percentual', 'vencedores', 'total']
grouped_multiple = grouped_multiple.reset_index()
print(grouped_multiple)

primeiras = [2.7,10.8]
ultimas = [9.3,2.1]

x1 =  np.arange(len(primeiras))
x2 = [x + 0.15 for x in x1]

# Plota as barras
plt.bar(x1, primeiras, width=0.15, label = '10 Primeiras Edições', color = 'gray')
plt.bar(x2, ultimas, width=0.15, label = '11 Últimas Edições', color = 'brown')

genero = ['Feminino','Masculino']
plt.xticks([x for x in range(len(primeiras))], genero)

# inseri uma legenda no gráfico
plt.legend()

plt.title("Percentual de Participantes Vencedores")
plt.show()

# Análise de Correlação entre Idade e Finalista a partir de Gráfico de Densidade
fig = plt.figure(figsize=(14,6))
ax=sns.kdeplot(df.loc[(df['finalista']==1),'idade'],color='g',shade=True)
ax=sns.kdeplot(df.loc[(df['finalista']==0),'idade'],color='r',shade=True)
# plt.title('Análise de Correlação entre Idade e Finalista a partir de Gráfico de Densidade')

# Análise de posição, genêro e últimas ediçõoes
fig = plt.figure(figsize=(6,8))

sns.boxplot(x='genero',y='posicao',data=df,color='c',hue="ultimas_edicoes")

fig = plt.figure(figsize=(6,8))

sns.boxplot(x='genero',y='eliminacao',data=df,color='y',hue="ultimas_edicoes")

fig = plt.figure(figsize=(14,8))

sns.boxplot(x='cor',y='eliminacao',data=df,color='orange')

fig = plt.figure(figsize=(6,8))

sns.boxplot(x='camarote',y='eliminacao',data=df,color='m')

fig = plt.figure(figsize=(16,8))

sns.boxplot(x='cat_profissional',y='eliminacao',data=df,color='c')

fig = plt.figure(figsize=(16,8))

sns.boxplot(x='cat_profissional',y='posicao',data=df,color='c')

sns.lmplot(x='idade',y='eliminacao',data=df,fit_reg=False,hue='regiao_nasc',palette='Set2',height=7)

# Copiando um novo dataset para transformação de variáveis qualitativas
dfa = df.copy()

dfa['cat_profissional'].replace(['Artes e Design','Administração e Serviços','Ciências Sociais e Humanas','Comunicação e Informação',
                    'Saúde e Bem-estar','Ciências Exatas e Engenharia'],
                   [0,1,2,3,4,5],inplace=True)
dfa['lgbtqia'].replace(['Não','Sim'],[0,1],inplace=True)
dfa['camarote'].replace(['Não','Sim'],[0,1],inplace=True)
dfa['cor'].replace(['Branca','Preta','Parda','Amarela','Indígena'],[0,1,2,3,4],inplace=True)
dfa['regiao_nasc'].replace(['Sudeste','Centro-Oeste','Nordeste','Sul','Norte', 'Estrangeiro'],[0,1,2,3,4,5],inplace=True)
dfa['genero'].replace(['Masculino','Feminino'],[0,1],inplace=True)

plt.figure(figsize=(16,8))

correlacao = dfa.corr()
correlacao = (correlacao)
sns.heatmap(correlacao,xticklabels=correlacao.columns.values,yticklabels=correlacao.columns.values,annot=True,vmin=-1,vmax=1,cmap='coolwarm',linewidths=0)

correlacao

# Análise de correlações entre variáveis
pd.crosstab(df["cor"],df["finalista"],margins=True)

cat_profissional = df.groupby('cat_profissional')
cat_profissional.mean()
#'Artes e Design' 0,'Administração e Serviços' 1,'Ciências Sociais e Humanas' 2,'Comunicação e Informação' 3,
#                    'Saúde e Bem-estar' 4,'Ciências Exatas e Engenharia' 5

df.head()

c = df['vencedor'].value_counts()
p = df['vencedor'].value_counts(normalize=True)
pd.concat([c,p], axis=1, keys=['counts', '%'])

c = df['finalista'].value_counts()
p = df['finalista'].value_counts(normalize=True)
pd.concat([c,p], axis=1, keys=['counts', '%'])

# Instalação de um módulo a ser utilizado
!pip install category_encoders

from category_encoders.one_hot import OneHotEncoder

# Transformando a coluna gênero
enc = OneHotEncoder(cols=['genero'], use_cat_names=True)
df = enc.fit_transform(df)

# Transformando a coluna cor
enc = OneHotEncoder(cols=['cor'], use_cat_names=True)
df = enc.fit_transform(df)

# Transformando a coluna lgbtqia
enc = OneHotEncoder(cols=['lgbtqia'], use_cat_names=True)
df = enc.fit_transform(df)

# Transformando a coluna cat_profissional
enc = OneHotEncoder(cols=['cat_profissional'], use_cat_names=True)
df = enc.fit_transform(df)

# Transformando a coluna camarote
enc = OneHotEncoder(cols=['camarote'], use_cat_names=True)
df = enc.fit_transform(df)

# Transformando a coluna regiao_nasc
enc = OneHotEncoder(cols=['regiao_nasc'], use_cat_names=True)
df = enc.fit_transform(df)

df.head()

plt.figure(figsize=(28,22))

correlacao = df.corr()
correlacao = (correlacao)
sns.heatmap(correlacao,xticklabels=correlacao.columns.values,yticklabels=correlacao.columns.values,annot=True,vmin=-1,vmax=1,cmap='coolwarm',linewidths=0)

correlacao

# Remoção de colunas não significativas ao modelo de previsão
df_mdl = df.drop(['edicao', 'ano_edicao', 'nome', 'data_nascimento', 'profissao', 'cidade_nasc', 'estado_nasc', 'colocacao', 'indicacao', 'eliminacao', 'final', 'finalista', 'vencedor'],axis = 1)

# Análise de variáveis que contém registros vazios
df_mdl.isnull().sum()

# Remoção de registros que contém dados vazio
df_mdl.dropna(inplace=True)

# Separando as variáveis entre preditoras e alvo
alvop = df_mdl['posicao']
alvor = df_mdl['rejeicao']
pred = df_mdl.drop(['posicao','rejeicao'],axis = 1)

# Criando os conjuntos de dados de treino e teste
from sklearn.model_selection import train_test_split

predr_treino, predr_teste, alvor_treino, alvor_teste = train_test_split(pred, alvor, test_size = 0.2)

predp_treino, predp_teste, alvop_treino, alvop_teste = train_test_split(pred, alvop, test_size = 0.2)

# Criação dos modelos
from sklearn.ensemble import RandomForestRegressor
mdlp = RandomForestRegressor(n_estimators=100)
mdlp.fit(predp_treino, alvop_treino)

# Criação dos modelos
from sklearn.ensemble import RandomForestRegressor
mdlr = RandomForestRegressor(n_estimators=100)
mdlr.fit(predr_treino, alvor_treino)

# Analisando a importância de cada variável preditora para a geração de valor da variável alvo
mdlp.feature_importances_

# Analisando a importância de cada variável preditora para a geração de valor da variável alvo
mdlr.feature_importances_

# Aplicação do modelo para o conjunto de dados teste
previsoes_posicao = mdlp.predict(predp_teste)
previsoes_posicao

# Aplicação do modelo para o conjunto de dados teste
previsoes_rejeicao = mdlr.predict(predr_teste)
previsoes_rejeicao

# Avaliação do modelo com MAE
from sklearn.metrics import mean_absolute_error
mean_absolute_error(alvop_teste, previsoes_posicao)

mean_absolute_error(alvor_teste, previsoes_rejeicao)

# Verificação e comparação dos resultados dos três primeiros registros do conjunto de dados teste
previsoes_posicao[0:10]

alvop_teste[0:10]

# Verificação e comparação dos resultados dos três primeiros registros do conjunto de dados teste
previsoes_rejeicao[0:10]

alvor_teste[0:10]