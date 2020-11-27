# !-- 빅데이터 처리하는 코드를 여기서 하면 됩니다
# 1. 크롤링
#    1. https://movie.naver.com/movie/point/af/list.nhn
#    2. 제목, 평점, 리뷰 가져오기
# 2. 지도 그리기
# 3. 그래프 그리기
# ----- ----- ----- ----- -----
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt # 그래프 그릴 때 필요한 것
from matplotlib import font_manager, rc # 한글 적용에 필요한 것
import os
import pandas as pd
import numpy as np
import requests # 다른 페이지에 넘어갈? 접속할? 때 필요한 것

from pyboard.settings import STATIC_DIR, TEMPLATE_DIR
from konlpy.tag._okt import Okt
from collections import Counter
import pytagcloud
import folium
from folium import plugins
    
def movie_crawling(data):
    for i in range(5): # 영화 페이지 100page를 crawling합니다
        url='https://movie.naver.com/movie/point/af/list.nhn?&page='   # page 한 번 눌러서 page번호가 들어간 url을 적용
        url=url+str(i+1)    # 1~100 page까지의 url을 만듭니다
        req=requests.get(url)   # 해당 url의 내용을 가져옵니다
        print(req)
        if req.ok : # 200이면
            html=req.text # dom을 html에 넣습니다
            soup=BeautifulSoup(html, "html.parser")
            
            # title의 selector ==> #old_content > table > tbody > tr:nth-child(1) > td.title > a.movie.color_b
            # 여기서 젤 끝 어느정도 구분할 수 있는 정도만 적어주면 됩니다
            titles=soup.select(".title a.movie")   # title을 가져옵니다
            # select_one이면 한 개 가져오는데 select는 다 가져옵니다
            
            # point의 selector ==> #old_content > table > tbody > tr:nth-child(1) > td.title > div > em
            points=soup.select(".title em")
            
            # content의 selector ==> #old_content > table > tbody > tr:nth-child(1) > td.title
            # 이 타이틀 안의 내용이라서 .title만 해도 가져와진다
            contents=soup.select(".title")

            n=len(titles) # 한 page당 10개의 댓글들이 있어서 n=10
            
            for i in range(n):  # 댓글 10개의 내용들을 하나의 list에 담음
                title=titles[i].get_text()
                point=points[i].get_text()
                content_arr=contents[i].get_text().replace('신고', "").split('\n\n') # 신고는 지우고 줄 별로 split
                content=content_arr[2].replace("\t","").replace("\n","")    # 공백을 지운다
                data.append([title,point,content])  # 댓글의 정보를 가지고있는 list를 만든다
                
def make_graph(titles,points):
    # 한글 font 처리
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    
    # chart 그리기
    plt.xlabel('영화제목')
    plt.ylabel('평균평점')
    plt.grid(True)  # grid 표시하겠다
    plt.bar(range(len(titles)), points, align='center')
    # bar chart를 그린다 / x축, y축, center에 놓는다
    plt.xticks(range(len(titles)), list(titles), rotation='70')
    # x축에 title을 넣는데 겹치니까 70도 회전해서 넣는다
    plt.savefig(os.path.join(STATIC_DIR,'images/fig01.png'), dpi=300)
    # 저장한다 (경로, dpi=300)
    # STATIC_DIR 이걸 위해 settings에서  
    # 1. BASE_DIR 아래 줄에 TEMPLATE_DIR=os.path.join(BASE_DIR, 'board/tamplates') 추가
    # 2. STATIC_URL 아래 줄에 STATIC_DIR = os.path.join(BASE_DIR, 'board/static')
    # 각각의 DIR은 BASE_DIR + 뒤에 적은 path를 join한다
    

    
def saveWordcloud(contents):
    nlp = Okt()
    wordtext=""
    for t in contents:
        wordtext+=str(t)+" "
        
    nouns = nlp.nouns(wordtext)
    count = Counter(nouns)
    
    wordInfo = dict()
    for tags, counts in count.most_common(100):
        if (len(str(tags)) > 1):
            wordInfo[tags] = counts
    filename=os.path.join(STATIC_DIR,'images/wordcloud01.png')
    
    taglist = pytagcloud.make_tags(dict(wordInfo).items(), maxsize=80)
    pytagcloud.create_tag_image(taglist, filename, size=(640, 480), fontname='Korean', rectangular=False)
    
    
def cctv_map():
    popup=[]
    data_lat_log=[]
    df=pd.read_csv("e:/cctv.csv",encoding="utf-8")
    for data in df.values:
        if data[4]>0:
            popup.append(data[2])
            data_lat_log.append([data[3],data[4]])
    
    m=folium.Map([35.1803305,129.0516257], zoop_start=11)
    plugins.MarkerCluster(data_lat_log,popups=popup).add_to(m)
    m.save(os.path.join(TEMPLATE_DIR,"map/map01.html"))   
    
    
    
    
    
    
    