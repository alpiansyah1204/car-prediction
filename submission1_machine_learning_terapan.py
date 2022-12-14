# -*- coding: utf-8 -*-
"""Submission1  Machine Learning Terapan.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hsFM8Y_ELyZf7mexNscOYIC8TyRqCUxM

# Import Library

Mengimport Library untuk melakukan Exploratory Data Analisis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from io import BytesIO
import requests
import plotly.express as px

"""# Import Kaggle"""

pip install -q kaggle

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!ls ~/.kaggle

!kaggle datasets download -d adityadesai13/used-car-dataset-ford-and-mercedes

!unzip /content/used-car-dataset-ford-and-mercedes.zip

"""# IMPORT DATASET"""

df=pd.read_csv('vw.csv')
df

"""# EXPLORATORY DATA ANALYSIS (EDA) & DATA CLEANING

Disini saya melakukan Eksplorasi Data Analyis (EDA) dan Data Cleaning untuk memeriksa dataset yang akan saya training. Tujuannya adalah untuk melihat isi dari dataset tersebut apakah ada yang perlu dibuang atau tidak, apakah ada NaN, melihat tipe datanya, melihat jumlah kolom dan baris dan lainnya.
"""

print('===================EXPLORATORY DATA ANALYSIS=================================')
long_string='========================================================================'
def printByInformation(dataset, option=False):
  if option:
    pd.set_option('display.max_columns',None)
    print(f'current col:{dataset.shape[0]}')
    print(f'current rows:{dataset.shape[1]}')
    print(long_string)
    print('======================DATA CLEANING=======================================')
    print(f'jumlah NaN {dataset.isnull().sum().sum()} dari NaN yg ditemukan')
    print(long_string)
    print(f'jumlah NaN tiap Column\n{dataset.isnull().sum()}')
    print(long_string)
    print(f'Name Columns: {list(dataset.columns)}')
    print(long_string)
    print(f'{dataset.info()}')
    print(long_string)
    print(f'{dataset.describe()}')
printByInformation(df,True)

df.head()#melihat 5 data

"""# MEMERIKSA DATA YANG UNIK

melihat data Unique untuk mempermudah nanti saat melakukan analisis data dan juga preprocessing
"""

df['model'].unique()

df['transmission'].unique()

df['fuelType'].unique()

"""# DATA VISUALIZATION

melakukan visualisasi data untuk mempermudah membaca data dari segi bentuk visual sehingga lebih mudah dalam menganalisis data
"""

def identifyColumns(dataset,column,scatterPlot=False):
	print(f"Summary from column : {column}")
	print(f"Column type : {dataset[column].dtype}")
	print(long_string) 
	print(f"NaN  : {dataset[column].isna().sum()} From {len(dataset[column].values)} Observations")
	print(f"Unique Labels \n{dataset[column].unique()}")
	print(long_string)
	if(len(dataset[column].unique()) > 10):
		top10 = dataset[column].value_counts().head(10)
		sns.countplot(dataset[dataset[column].isin(top10.index)][column],label=column)
		plt.title(f"Barplot {column} Top 10")
		plt.show()
	else:
		sns.countplot(dataset[column],label=column)
		plt.title(f"Barplot {column}")
		plt.show()
	print(long_string)	
	print("Informasi General Dataset ...")
	print(df[column].describe())
	print(long_string)

	if(scatterPlot and dataset[column].dtype != 'object'):
		fig = go.Figure()
		fig.add_traces(go.Scatter(x = dataset[column],y=np.linspace(0,1,len(dataset[column].values)),mode='markers',name=column))
		fig.update_layout(title=f"Scatter Plot {column}",xaxis_title=column,
		yaxis_title='Range Values',height= 500,width=800)
		fig.show()
	
		 
identifyColumns(df, "transmission",True)
# Apabila liat Unbalanced , Coba buat dataset yang proporsi nya sama , File csv/excel dibedain 
# Gunakan Stratified CrossValidation

"""Insight yang saya dapatkan disini yaitu:
* lebih banyak yang menggunakan Manual transmission dibanding menggunakan Semi-Auto dan juga Automatic
* pengguna Automatic paling sedikit digunakan
* lebih banyak yang menggunakan Semi-Auto ketimbang Automatic
"""

def identifyColumns(dataset,column,scatterPlot=False):
	print(f"Summary from column : {column}")
	print(f"Column type : {dataset[column].dtype}")
	print(long_string) 
	print(f"NaN  : {dataset[column].isna().sum()} From {len(dataset[column].values)} Observations")
	print(f"Unique Labels \n{dataset[column].unique()}")
	print(long_string)
	if(len(dataset[column].unique()) > 10):
		top10 = dataset[column].value_counts().head(10)
		sns.countplot(dataset[dataset[column].isin(top10.index)][column],label=column)
		plt.title(f"Barplot {column} Top 10")
		plt.show()
	else:
		sns.countplot(dataset[column],label=column)
		plt.title(f"Barplot {column}")
		plt.show()
	print(long_string)	
	print("Informasi General Dataset ...")
	print(df[column].describe())
	print(long_string)

	if(scatterPlot and dataset[column].dtype != 'object'):
		fig = go.Figure()
		fig.add_traces(go.Scatter(x = dataset[column],y=np.linspace(0,1,len(dataset[column].values)),mode='markers',name=column))
		fig.update_layout(title=f"Scatter Plot {column}",xaxis_title=column,
		yaxis_title='Range Values',height= 500,width=800)
		fig.show()
	
		 
identifyColumns(df, "fuelType",True)
# Apabila liat Unbalanced , Coba buat dataset yang proporsi nya sama , File csv/excel dibedain 
# Gunakan Stratified CrossValidation

"""Insight yang saya dapatkan disini yaitu:
* Bensin Petrol yang paling banyak digunakan
* Bensin Diesel merupakan yang paling banyak kedua.
* yang menggunakan merek bensin lain selain Diesel dan Petrol ataupun Hybrid jarang sekali.
"""

df.info()

df.head()



temp=df.groupby('model')['year','price','tax','model'].sum().reset_index()
fig=go.Figure(data=[
    go.Bar(name='price', x=temp['model'],y=temp['price']),
    go.Bar(name='tax', x=temp['model'],y=temp['tax']),
])
fig.update_layout(
width=1000,
height=600,
barmode='stack',
title='Total case over time',
font=dict(size=14,color='#686868'),
xaxis_tickangle=-45,
yaxis=dict(
title='Count'))
fig.show()

"""Top 3 Mobil Golf, Tiguan dan juga Polo merupakan mobil yang sering digunakan pada kumpulan data dari semua mobil di VW"""

plt.figure(figsize=(15,5),facecolor='w') 
sns.barplot(x = df["year"], y = df["price"])

df.head()

"""jika dilihat pada tahun 2019 dan 2020 merupakan tahun yang dimana jumlah pembeli mobil VW terbanyak"""

sns.pairplot(df,x_vars=['model','year','transmission','mileage','fuelType','tax','mpg','engineSize'],y_vars=['price'])

"""disini saya menggunakan pairplot untuk melihat grafik mana yang memiliki kesamaan sehingga akan mempermudah untuk melakukan prediksi"""



"""# Feature Engineering

disini saya akan melakukan feature engineering untuk melihat apakah ada data yang dapat dibuat fitur baru sehingga akan memberikan kualitas data yang baik untuk melakukan prediksi
"""

df['age_car']=2020-df['year']
df

df=df.drop(columns=['year'])
df.head()

"""disini saya mendrop kolom 'year' karena menurut saya jika memakai kolom year akan memberikan efek pada data sehingga membuat kualitas data tersebut tidak sempurna karena dalam bentuk tahun sehingga dengan membuat fitur baru menjadi Age_car akan mempermudah dalam preprocessing dan memberikan kualitas data yang baik juga

# Data Preprocessing

disini saya akan melakukan data preprocessing sehingga data tersebut dapat di training dan akan menghasilkan hasil prediksi yang baik karena banyak sekali data yang harus diolah seperti pada kolom model yang dimana tipe datanya object atau string sehingga perlu diubah ke integer atau ke angka 0 dan 1 agar dapat diprediksi tanpa mendrop kolom tersebut.
"""

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df_new=pd.get_dummies(df,columns=['model','transmission','fuelType'])
df_new.head()

"""disini saya melakukan get dummies untuk merubah nilai object menjadi kategorikal sehingga dapat di training.

# Normalize

disini saya melakukan normalisasi agar semua nilai seperti nilai nominal, nilai int dan nilai float akan bernilai sama sehingga akan memberikan data yang baik
"""

scaler=StandardScaler()
df_scaler=scaler.fit_transform(df_new)
df_scaler=pd.DataFrame(df_scaler,columns=df_new.columns)
print(df_scaler.shape)

df_scaler.head()

X=df_scaler.drop(columns=['price'])
y=df_scaler['price']

"""# Modelling and Training"""

X_train,X_test,Y_train,Y_test=train_test_split(X,y)

linreg=LinearRegression()
linreg.fit(X_train,Y_train)
y_pred=linreg.predict(X_test)
print('Slope:',linreg.intercept_)
print('coefficient:',linreg.coef_)
print('nilai score',linreg.score(X_test,Y_test))

from sklearn.metrics import r2_score,mean_squared_error

"""# Conclusion Report"""

print('mse:',mean_squared_error(Y_test,y_pred))
print('rmse:',np.sqrt(mean_squared_error(Y_test,y_pred)))
print('r^2:',r2_score(Y_test,y_pred))



"""# Modelling

disini saya mendapatkan score prediksi yang baik yaitu sebesar 0.885 atau 88.5% sehingga masih cukup baik untuk prediksi tetapi itu masih standar sehingga masih banyak yang harus dirubah pada modelling
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR

column_names=df_new.drop(columns=['price']).columns

no_of_features = []
r_squared_train = []
r_squared_test = []

for k in range(3, 40, 2):
    selector = SelectKBest(f_regression, k = k)
    X_train_transformed = selector.fit_transform(X_train, Y_train)
    X_test_transformed = selector.transform(X_test)
    regressor = LinearRegression()
    regressor.fit(X_train_transformed, Y_train)
    no_of_features.append(k)
    r_squared_train.append(regressor.score(X_train_transformed, Y_train))
    r_squared_test.append(regressor.score(X_test_transformed, Y_test))
    
sns.lineplot(x = no_of_features, y = r_squared_train, legend = 'full')
sns.lineplot(x = no_of_features, y = r_squared_test, legend = 'full')

"""disini saya mencoba untuk menebak berapa jumlah variabel yang terbaik agar dapat menghasilkan prediksi yang baik dan ternyata dengan KBest saya dapat mendapatkan prediksi yang baik dengan 23 variabel yaitu 0.88 seperti dengan pengujian model pertama."""

selector = SelectKBest(f_regression, k = 23)
X_train_transformed = selector.fit_transform(X_train, Y_train)
X_test_transformed = selector.transform(X_test)
column_names[selector.get_support()]

def regression_model(model):
    regressor = model
    regressor.fit(X_train_transformed, Y_train)
    score = regressor.score(X_test_transformed, Y_test)
    return regressor, score

"""# Prediction"""

model_performance = pd.DataFrame(columns = ["Features", "Model", "Score"])

models_to_evaluate = [LinearRegression(), Ridge(), Lasso(), SVR(), RandomForestRegressor(), MLPRegressor()]

for model in models_to_evaluate:
    regressor, score = regression_model(model)
    model_performance = model_performance.append({"Features": "Linear","Model": model, "Score": score}, ignore_index=True)

model_performance

"""disini saya mencoba untuk prediksi dengan menggunakan banyak model dan ternyata model tertinggi didapatkan oleh DecisionTreeRegressor dengan score tertinggi 0.947823"""

poly = PolynomialFeatures()
X_train_transformed_poly = poly.fit_transform(X_train)
X_test_transformed_poly = poly.transform(X_test)

print(X_train_transformed_poly.shape)

no_of_features = []
r_squared = []

for k in range(10, 277, 5):
    selector = SelectKBest(f_regression, k = k)
    X_train_transformed = selector.fit_transform(X_train_transformed_poly, Y_train)
    regressor = LinearRegression()
    regressor.fit(X_train_transformed, Y_train)
    no_of_features.append(k)
    r_squared.append(regressor.score(X_train_transformed, Y_train))
    
sns.lineplot(x = no_of_features, y = r_squared)

"""disini saya ingin mencoba dengan polynomial features sebagai preprocesingnya dan ternyata dengan polynomial memberikan akurasi yang besaryaitu 0.94 dengan dengan K sekitar 110 an dan disini saya mencoba dengan K=110"""

selector = SelectKBest(f_regression, k = 110)
X_train_transformed = selector.fit_transform(X_train_transformed_poly, Y_train)
X_test_transformed = selector.transform(X_test_transformed_poly)

"""# Conclusion"""

models_to_evaluate = [LinearRegression(), Ridge(), Lasso(), SVR(), RandomForestRegressor(), MLPRegressor()]

for model in models_to_evaluate:
    regressor, score = regression_model(model)
    model_performance = model_performance.append({"Features": "Polynomial","Model": model, "Score": score}, ignore_index=True)

model_performance

"""Dengan menggunakan Polynomial terbukti memberikan hasil yang terbaik yaitu sebesar 0.951851 dengan begitu, hasil prediksi saya akan memberikan prediksi yang baik karena sudah diatas 93% yaitu 95%"""
