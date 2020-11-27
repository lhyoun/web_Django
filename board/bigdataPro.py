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
                
         


