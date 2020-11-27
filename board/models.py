from django.db import models
from datetime import datetime

class Board(models.Model):
    idx=models.AutoField(primary_key=True)
    writer=models.CharField(null=False,max_length=50)
    title=models.CharField(null=False,max_length=200)
    content=models.TextField(null=False)
    hit=models.IntegerField(default=0)
    post_date=models.DateTimeField(default=datetime.now,blank=True)
    
    filename=models.CharField(null=True,blank=True,default="",max_length=500)
    filesize=models.IntegerField(default=0)
    down=models.IntegerField(default=0)
    
    def hit_up(self):
        self.hit+=1
    def down_up(self):
         self.down+=1
     
 
 #댓글 테이블
class Comment(models.Model):
    #댓글 글번호
    idx=models.AutoField(primary_key=True)
    #게시물 번호
    board_idx=models.IntegerField(null=False)
    writer=models.CharField(null=False,max_length=50)
    content=models.TextField(null=False)
    post_date=models.DateTimeField(default=datetime.now,blank=True)
    