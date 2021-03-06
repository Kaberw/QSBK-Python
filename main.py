#-*- coding:utf-8 -*-
#@author:kaber

import urllib
import urllib2
import re
import thread
import time

class QSBK:
 def __init__(self):
  self.pageIndex = 1
  self.user_agent = '(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
  self.headers = {'User-Agent':self.user_agent}
  self.stories = []
  self.enable = False
  
 def getPage(self,pageIndex):
  try:
   url = r'https://www.qiushibaike.com/article/'+str(self.pageIndex)
   request = urllib2.Request(url,headers = self.headers)
   response = urllib2.urlopen(request)
   pageCode = response.read().decode('utf-8')
   return pageCode 
  except urllib2.URLError,e:
   if hasattr(e,"reason"):
    print u"连接失败，错误原因：",e.reason
   return None
 
 def getPageItems(self,pageIndex):
  pageCode = self.getPage(pageIndex)
  if not pageCode:
   print "页面加载失败..."
   return None
  pattern = re.compile('<div.*?content">(.*?)</div>.*?<div class="stats.*?class="number">(.*?)</i>.*?<i class="number">(.*?)</i>',re.S)#(.*?)</div>
  items = re.findall(pattern,pageCode)
  pageStories = []
  for item in items:
   #haveImg = re.search('img', item[1])
   #if haveImg:
    #print u"含有图片,无法显示\n"
   #if not haveImg:
   replaceBR = re.compile('<br/>')
   text = re.sub(replaceBR,"\n",item[0])
   pageStories.append([text.strip(), item[1].strip(), item[2].strip()])
  return pageStories
 
 def loadPage(self):
  if self.enable == True:
   if len(self.stories)<2:
    pageStories = self.getPageItems(self.pageIndex)
    if pageStories:
     self.stories.append(pageStories)
     self.pageIndex += 1
 
 def getOneStory(self,pageStories,page):
  for story in pageStories:
   input = raw_input()
   self.loadPage()
   if input == "Q":
    self.enable == False
    return
   print u"第%d页\t好笑数:%s\t评论:%s\n%s" %(page,story[1],story[2],story[0])
 
 def start(self):
  print u"正在读取，按回车查看下一条,Q退出"
  self.enable = True
  self.loadPage()
  nowPage = 0
  while self.enable:
   if len(self.stories)>0:
    pageStories = self.stories[0]
    nowPage += 1
    del self.stories[0]
    self.getOneStory(pageStories,nowPage)
 

spider = QSBK()
spider.start()
