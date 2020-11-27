import os

from anaconda_navigator.utils.py3compat import request
from django.contrib.sessions.backends import file
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt

from board.models import Board, Comment, Movie
from django.db.models import Q
import math
from board import bigdataPro


# Create your views here.
def main(request):
    return render(request, "main.html")

def movie_save(request):
    data=[]
    bigdataPro.movie_crawling(data)
    for row in data:
        dto=Movie(title=row[0], point=row[1], content=row[2])
        dto.save()
    return redirect("/")

def write(request):
    return render(request,"write.html")


def list(request):
    boardCount=Board.objects.count()
#board table에 있는 모든 record를 다 가져오고 idx별로 역순으로 정렬해라 
    boardList=Board.objects.all().order_by("-idx")
    
#검색옵션, 검색값
    try: #예외가 발생할 가능성이 있는 코드
        search_option = request.POST["search_option"]
    except: #예외가 발생했을 때의 코드
        search_option = "writer"
    
    try:
        search= request.POST["search"]
    except:
        search = ""
    
    
    print("search_option:",search_option)
    print("search:",search)
    #레코드 갯수 계산
    # 필드명__contains=값 => where 필드명 like '%값%'
    # count() => select count(*)
#---------------------------레코드 개수 구하기 끝 --------------------------------- 
    if search_option == "all": #이름+제목+내용
         #Q는 option과 같은 것이다. 
        boardCount = Board.objects.filter(Q(writer__contains=search) | Q(title__contains=search)|  Q(content__contains=search)).count()
    elif search_option == "writer": #이름
            boardCount = Board.objects.filter(writer__contains=search).count()
    elif search_option == "title": #제목
            boardCount = Board.objects.filter(title__contains=search).count()
    elif search_option == "content": #내용
        boardCount = Board.objects.filter(content__contains=search).count()
    # limit start,레코드갯수
#---------------------------레코드 개수 구하기 끝 ---------------------------------
    try:
#start값이 있으면 
        start = int(request.GET['start'])
    except:
#없으면 0으로 
        start = 0
#----------------------------------------------------------------------------------------
    
    page_size = 10; # 페이지당 게시물수
    page_list_size = 10; # 한 화면에 표시할 페이지의 갯수
    end=start+page_size
    #전체 페이지 갯수 , math.ceil() 올림함수 #math 는 수학 module 
    total_page = math.ceil(boardCount / page_size)
    #start 레코드시작번호 => 페이지번호
    current_page = math.ceil( (start+1) / page_size )
    #페이지 블록의 시작번호, math.floor() 버림함수
                #ex) 만약 15면 floor하면 1이 된다. 
    start_page = math.floor((current_page - 1) / page_list_size ) * page_list_size+ 1;
    #페이지 블록의 끝번호
    end_page = start_page + page_list_size - 1;
    #마지막 페이지가 범위를 초과하지 않도록 처리
#------------------------------------------------------------------------------------------------
    if total_page < end_page:
        end_page = total_page
    # 1 ~ 10
   # [이전] 11 ~ 20
#
    if start_page >= page_list_size:
        prev_list = (start_page - 2) * page_size;
    else:
        prev_list = 0
    # 91 ~ 100 ,
    # 81 ~ 90 [다음]
    if total_page > end_page:
        next_list = end_page * page_size
    else:
        next_list = 0
        
        
        
    #레코드 내용
# 리스트[start:end] => start~end-1
    if search_option=="all":
        boardList = Board.objects.filter(Q(writer__contains=search) | Q(title__contains=search) |  Q(content__contains=search)).order_by("-idx")[start:end]
    elif search_option=="writer":
        boardList = Board.objects.filter(writer__contains =
        search).order_by("-idx")[start:end]
    elif search_option=="title":
        boardList = Board.objects.filter(title__contains =
        search).order_by("-idx")[start:end]
    elif search_option=="content":
        boardList = Board.objects.filter(content__contains =
        search).order_by("-idx")[start:end]
    print("start_page:",start_page)
    print("end_page:",end_page)
    print("page_list_size:",page_list_size)
    print("total_page:",total_page)
    print("prev_list:",prev_list)
    print("next_list:",next_list)
    links=[]
    # range(start_page,end_page+1) start_page~end_page
    # str(숫자변수) => 숫자변수를 스트링변수로
    for i in range(start_page,end_page+1):
        page = (i - 1) * page_size
        #완성된 tag형태를 links에 가져다 놓음. 나중에 links만 가져도 놓을 수 있음. 
        #
        links.append("<a href='?start="+str(page)+"'>"+str(i)+"</a>")
    
    return render(request, "list.html",\
    {"boardList": boardList, "boardCount": boardCount,\
    "search_option": search_option, "search": search,\
    "range":range(start_page-1,end_page),\
    "start_page":start_page,"end_page":end_page,\
    "page_list_size":page_list_size, "total_page":total_page,\
    "prev_list":prev_list,"next_list":next_list,\
    "links":links})





UPLOAD_DIR="e:/" #upload 폴더
@csrf_exempt
def insert(request):
    fname = ""
    fsize = 0
    if "file" in request.FILES:
        file=request.FILES["file"]
    fname = file.name
    fsize = file.size
    fp=open("%s%s" % (UPLOAD_DIR, fname), "wb")
    for chunk in file.chunks():
        fp.write(chunk)
        fp.close()
    
    dto = Board( writer=request.POST["writer"],title=request.POST["title"],\
    content=request.POST["content"], filename=fname,filesize=fsize )
    dto.save()
    print(dto)
    return redirect("/") 



def download(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    path=UPLOAD_DIR+dto.filename
    filename=os.path.basename(path)
    filename=filename.encode('utf-8')
    filename=urlquote(filename)
    with open(path, 'rb') as file:
        response=HttpResponse(file.read(),
                              content_type="application/octet-stream")
        response['Content-Disposition']=\
        "attachment;filename*=UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save()
        return response
    

def detail(request):
    #조회수 증가 처리
    id=request.GET["idx"]
    dto=Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    commentList = Comment.objects.filter(board_idx = id).order_by("idx")
    print("filesize:",dto.filesize)
    #filesize = "%0.2f" % (dto.filesize / 1024)
    filesize = "%.2f" % (dto.filesize)
    return render(request, "detail.html", {"dto": dto, "filesize":filesize, "commentList":commentList }) 

@csrf_exempt
def reply_insert(request):
    id=request.POST["idx"] #게시물 번호
    #댓글 객체 생성
    dto = Comment(board_idx=id,\
    writer=request.POST["writer"],\
    content=request.POST["content"])
    #insert query 실행
    dto.save()
    # detail?idx=글번호 페이지로 이동
    return HttpResponseRedirect("detail?idx="+id)

@csrf_exempt
def delete(request):
    id=request.POST["idx"] #삭제할 게시물의 번호
    Board.objects.get(idx=id).delete() #레코드 삭제
    return redirect("/") #시작 페이지로 이동
 
@csrf_exempt
def update(request):
    id=request.POST["idx"] #글번호
    #select * from board_board where idx=id
    dto_src=Board.objects.get(idx=id)
    fname=dto_src.filename #기존 첨부파일 이름
    fsize=0 #기존 첨부파일 크기
    if "file" in request.FILES: #새로운 첨부파일이 있으면
        file=request.FILES["file"]
        fname=file._name #새로운 첨부파일의 이름
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk) #파일 저장
        fp.close()
        #첨부파일의 크기(업로드완료 후 계산
        fsize=os.path.getsize(UPLOAD_DIR+fname)
        #수정 후 board의 내용
    dto_new = Board(idx=id, writer=request.POST["writer"], title=request.POST["title"],
    content=request.POST["content"], filename=fname, filesize=fsize)
    dto_new.save() #update query 호출
    return redirect("/") #시작 페이지로 이동


