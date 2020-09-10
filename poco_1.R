
# 1 : preparation ---------------------------------------------------------
suppressPackageStartupMessages({ 
  library(rgdal,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(ggmap,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(sp,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(maptools,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(viridis,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(magrittr,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(scales,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(gridExtra,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(data.table, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(tidyverse, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(lubridate, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(gridExtra, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(factoextra, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(tfplot, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(tsfa, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(factoextra, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(cluster, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(IRdisplay, warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(foreign,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(extrafont,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(showtext,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
  library(grid,warn.conflicts = FALSE, quietly = TRUE, verbose = FALSE)
})


setwd('C:/postcorona_DA/data')
getwd()
# 2 : EDA -----------------------------------------------------------------

# 2-1 ---------------------------------------------------------------------
# A. 코로나19 사태 기본 분석
# 지역별, 나이대별, 성별 확진자 시각화
# a. 지역별 확진자 시각화 해석
# 지역별 확진자의 비율을 파악해 보도록 하겠습니다. 
# 먼저, 어떤 지역이 코로나 심각 지역인지 알아보기 위해 지역별 확진자의 수를 지도 위에 표시해 보도록 하겠습니다.

# C:/postcorona_DA/data/ =>C:/postcorona_DA/data/

#행정구역 지도를 가져와 줍니다.
korea_map_shp = rgdal::readOGR("C:/postcorona_DA/data/지도/CTPRVN.shp")
korea_map = fortify(korea_map_shp)


korea_map %>% str()

#지역별 확진자 수를 지도에 표시하기 위해 확진자 수 데이터를 가져오고, 알맞게 전처리해 줍니다.

TimeProvince <-fread('C:/postcorona_DA/data/COVID_19/TimeProvince.csv',
                     stringsAsFactors=FALSE, 
                     encoding = "UTF-8")

TimeProvince$date <- as.Date(TimeProvince$date)
TimeProvince$date <- as.character(TimeProvince$date,'%m/%d')

TimeProvince$province=TimeProvince$province %>% as.factor()

confirm_added=TimeProvince %>%
  group_by(province)%>% 
  summarize(N=max(confirmed))

confirm_added$province=plyr::revalue(confirm_added$province,c("서울"="0","부산"="1","대구"="2",
                                                              "인천"="3","광주"="4","대전"="5",
                                                              "울산"="6","세종"="7","경기도"="8",
                                                              "강원도"="9","충청북도"="10","충청남도"="11",
                                                              "전라북도"="12","전라남도"="13","경상북도"="14",
                                                              "경상남도"="15","제주도"="16"))


colnames(confirm_added)<-c("id","confirmed")







