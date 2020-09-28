%matplotlib inline
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import plotly.io as pio
pio.renderers.default = 'notebook_connected'

import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

import csv
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

from itertools import product

#Matplotlib 한국어 세팅
import platform
from matplotlib import font_manager, rc

plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname='/Users/adonishan/Library/Fonts').get_name()
    rc('font', family=font_name)

 #palette
pal = ['#50d890', '#007944','#888888','#f3c623','#EFEFEF', '#96bb7c', '#d9bf77','#3f3f44']


def fig_cards():
	card = pd.read_csv('data/card_20200717.csv')
	card.columns = ['날짜', '행정동 코드', '행정동', '업종 코드', '업종', '판매건수', '판매금액']

	card['날짜'] = card['날짜'].astype('str').apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:])
	card['행정동 코드'] = card['행정동 코드'].astype('str').apply(lambda x:x [:-2]).astype('int')
	region.columns = ['행정동 코드','행정동','광역시도','시군구']
	region['행정동 코드'] = region['행정동 코드'].astype('int')
	card = pd.merge(card, region, on=['행정동 코드'], how = 'left')
	card = card[card['광역시도'] == '서울특별시']
	card = card.drop(['행정동 코드', '업종 코드'],axis=1)
	card = card.groupby(['날짜','업종']).sum().reset_index()
	date = list(card['날짜'].unique())
	category = list(card['업종'].unique())
	item = [date,category]
	card_temp = pd.DataFrame(product(*item), columns = ['날짜','업종'])

	card_compare = card.copy()

	card = pd.merge(card,card_temp,on=['날짜','업종'],how='right')

	card = card.fillna(0)

	card = card.groupby(['날짜','업종']).mean().reset_index()

	card = card.drop(['주'],axis=1)
	card['주'] = pd.to_datetime(card['날짜']).dt.week
	card = card.groupby(['업종','주']).mean().reset_index()

def weekly_card_graph():
	fig,ax = plt.subplots(1,2,figsize=(14,5))

	ax[0].plot(card_compare[card_compare['업종'] == '인터넷종합Mall']['판매금액'])
	ax[0].set_title("일별 인터넷종합Mall 판매건수", fontsize=15)
	ax[0].set_xticks([])

	ax[1].plot(card[card['업종'] == '인터넷종합Mall']['판매금액'])
	ax[1].set_title("주별 인터넷종합Mall 판매건수", fontsize=15)
	ax[1].set_xticks([])



