import requests
import os
import os.path as pth
from multiprocessing import Pool
from functools import partial
from tqdm.notebook import tqdm
import zipfile
import pandas as pd
import numpy as np
import plotly.io as pio
pio.renderers.default = 'notebook_connected'
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.colab import auth, drive

auth.authenticate_user()
drive.mount('/content/drive')



# using R in Python
import rpy2
%load_ext rpy2.ipython

from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import pandas as pd
pandas2ri.activate()
import rpy2.robjects as robjects

%%R
library(tidyverse)
library(lubridate)
library(dplyr)
# install.packages("reshape2")
library(reshape2)

## data
### card data
- c0
- c1

### person data
- po ==> p1


c0 <- read_csv("")
names(c0) <- c("date","loCode","loName","stCode","stType","cnt","amt")



%%R
c1 <- c0[,c(1,5:7)]
head(c1)

#na 값 없음
%%R
sum(is.na(c1))

%%R
#확진자 성별, 연령대, 확진일,완치일,사망일 데이터
#기존 PatientInfo.csv가 tab 분리임에도 쉽표 분리로 저장되어있어서 execel에서 저장형식을 바꾼 파일로 진행
p0 <- read_csv("/content/drive/My Drive/Colab Notebooks/dacon/data/COVID_19/PatientInfo_tab.csv") 
p1 <- select(p0, "sex", "age", "confirmed_date","released_date","deceased_date")

%%R
# p1 데이터중 na값 있는 것
p1[which(is.na(p1$confirmed_date)),]

- NA값 제거

%%R
p2 <- p1[-which(is.na(p1$confirmed_date)),] #na.omit 사용시 deceased_date때문에 데이터 대부분 날라감
dim(p1) #5165    5
dim(p2) #5162    5 (row 3개 사라짐)

%%R
p2$confirmed_date <- p2$confirmed_date %>% ymd() %>% as.POSIXct
p2$released_date <- p2$released_date %>% ymd() %>% as.POSIXct
p2$deceased_date <- p2$deceased_date %>% ymd() %>% as.POSIXct

%%R
head(p2)

### i. 건강,의료 관련으로 분류
- 의료용품 - 제약회사, 기타의료기관 의료기기
- 한약방 --홍삼 제품, 기타건강식
- 건강진단

%%R
#분류
cr <- c1 %>% filter(
  stType == '의료 용품' |stType == "기타의료기관및기타의료기기" |
    stType == "제약회사")

cf <- c1 %>% filter(
  stType == '한약방' |stType == "건강식품(회원제형태)" | stType == "인삼 제품"|
    stType == "홍삼 제품" |stType == "기타건강식")

ch <- c1 %>% filter(stType == '건강진단')

%%R
# 한약방 
head(cf)

### count(빈도)
- group by date
- sum count


cr_g <- cr %>% group_by(date) %>%
  summarise(count = sum(as.integer(cnt), na.rm = T), sales = sum(as.integer(amt), na.rm = T))
cf_g <- cf %>% group_by(date) %>%
  summarise(count = sum(as.integer(cnt), na.rm = T), sales = sum(as.integer(amt), na.rm = T))
ch_g <- ch %>% group_by(date) %>%
  summarise(count = sum(as.integer(cnt), na.rm = T), sales = sum(as.integer(amt), na.rm = T))

##### 한약방 (보약식품 개별 항목 추출)
- 한약방
- 인삼
- 홍삼
- 기타
- 회원제형식

%%R
# 그룹화 및 합산 function 제작
group_sum <- function(x, y) {
    x %>% filter(stType == y)  %>%  group_by(date) %>%
  summarise(count = sum(as.integer(cnt), na.rm = T), sales = sum(as.integer(amt), na.rm = T))
}


#보양식품 개별화
cfSep_om <- group_sum(c1, '한약방')
cfSep_is <- group_sum(c1, "인삼 제품")
cfSep_hs <- group_sum(c1, "홍삼 제품")
cfSep_ef <- group_sum(c1, "기타건강식")
cfSep_hf <- group_sum(c1, "건강식품(회원제형태)")

### h.count 생성- 건강 관련 제품들의 판매 횟수

%%R
hcount <- Reduce(function(x,y) full_join(x = x, y= y, by = "date"),
                list(select(cr_g,-sales), select(cf_g,-sales), select(ch_g,-sales)))

hcount <- arrange(hcount,date)

names(hcount) <- c('date','medSupply','healthFood','checkUp')

##### (1) 서식변경 lubridate==> posix

%%R
#date 서식으로 변경 
       #lubridate 안되어서 posix로 변경 #as.POSIXct 
       #재실행 후 posix origin요구하면 lubricate한번 했다가 다시 posix로 돌아가기
       
hcount$date <- ymd(hcount$date)       
hcount$date <- as.POSIXct(hcount$date)

%%R
head(hcount) #checkUp의 NA는 데이터 시작일자의 차이일뿐, 전체가 NA인 것은 아님

%%R
tail(hcount) #checkUp 데이터 존재 확인