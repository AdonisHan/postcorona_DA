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

#############

import card_region

card_region.fig_cards()
card_temp = card.copy()
# 첫 1,2,3 주
front_week = card_temp[(card_temp['주'].isin([1,2,3]))]

# 첫 1,2,3주의 외의 주
behind_week = card_temp[~(card_temp['주'].isin([1,2,3]))]
k1 = front_week.groupby(['업종']).mean()['판매건수'].median()
k2 = behind_week.groupby(['업종']).mean()['판매건수'].median()
kind = list(card['업종'].unique())

def plot_compare_weekly():
	fig, ax = plt.subplots(1,2,figsize=(14,5))
	kind = list(card['업종'].unique())
	 
	for i in range(0, len(set(card_temp['업종']))):
	    if i//10 == 0:
	        ax[0].plot(np.array(card_temp[card_temp['업종'] == kind[i]]['판매건수']),marker='o', linewidth=2)
	ax[0].set_title('업종들의 추이가 1~3주에서 최저', fontsize=15)
	ax[0].plot(1, 0.05, 'o', ms=60, mfc='none', color='g', mew=3)
	        
	x=['1~3주의 중앙값', '4~ 주의 중앙값']
	y=[k1,k2]
	ax[1].bar(x, y,  color=[pal[1],pal[5]])
	ax[1].set_title("1~3주와 4~ 주의 판매건수 비교", fontsize=15)

	plt.tight_layout()

plot_compare_weekly()