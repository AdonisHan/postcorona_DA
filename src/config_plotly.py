######## configure plotly.io

import pandas as pd 
import plotly.io as pio
pio.renderers.default = 'notebook_connected'

# /Users/adonishan/_Python/postcorona/KT_data_20200717
pd.options.plotting.backend = 'plotly'

## plotly.io를 import 한 후 renderers 기본값을 꼭 "notebook_connected" 로 설정해주시기 바랍니다.
import plotly.io as pio


### TEST
kt = pd.read_csv('./postcorona/KT_data_20200717/fpopl.csv')

kt['base_ymd'] = pd.to_datetime(kt['base_ymd'].astype('str'))

## 일자별 유동인구
kt[['base_ymd', 'popltn_cascnt']].groupby('base_ymd').sum().plot()

pio.renderers.default = "notebook_connected"

