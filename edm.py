import requests    
import  os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import shutil
import zipfile
from os.path import join, getsize
import time

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""
    
def get_EDM_Urls():
    url = 'https://edm.com/news'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    cards=[]
    for link in soup.find_all('a',attrs={"phx-track-id":"Title"}):
        cards.append(link['href'])
    return cards

def get_Txt(url,index):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    cards=[]

    contents=[]
    for link in soup.find_all('div',attrs={"class":"m-detail--body"}):
        pcontent=(link.find_all('p'))
        for pc in pcontent:
            contents.append(list(pc.stripped_strings))

 
    titles=[]
    for link in soup.find_all('div',attrs={"class":"m-detail-header--content"}):
        ptitle=(link.find_all())
        for pc in ptitle:
            titles.append(list(pc.stripped_strings))

    fo = open(str(index)+".txt", "w",encoding='UTF-8')
    fo.write("标题栏：")
    
    for a in titles:
        fo = open(str(index)+".txt", "a+",encoding='UTF-8')
        fo.write('\n')
        for b in a:
            fo.write(b)
            
    fo = open(str(index)+".txt", "a",encoding='UTF-8')
    fo.write("\n内容：")
    
    for a in contents:
        fo = open(str(index)+".txt", "a+",encoding='UTF-8')
        fo.write('\n')
        for b in a:
            fo.write(b)

def zip_file(src_dir):
    zip_name = src_dir +'.zip'
    date=time.strftime("%Y-%m-%d-%H:%M", time.localtime())
    z = zipfile.ZipFile(date,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        fpath = dirpath.replace(src_dir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('==压缩成功==')
    z.close()
def toZip(startdir):
    date=time.strftime("%Y-%m-%d-%H", time.localtime())
    file_news = date + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                print('压缩成功')
    z.close()
    return file_news
    


def main():
    urls=[]
    urls=get_EDM_Urls()
    a=1
    for url in urls:
        print(a)
        print(url)
        get_Txt(url,a)
        a=a+1        
    toZip(os.getcwd())

# filenames = os.listdir(os.getcwd())
# fo = open("foo.txt", "w")
# fo.write('hello python！')
# f=open('foo.txt','r')
# data_1=f.read()
# print(data_1)

main()
    