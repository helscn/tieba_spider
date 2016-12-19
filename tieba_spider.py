#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import codecs
from pyquery import PyQuery as pq

def parseBr(doc):
    '''将网页中的<br>标签替换为换行符'''
    return doc.find('br').replaceWith('\n').end()

def parseImg(doc):
    '''将网页中的<img>标签替换为Markdown格式的图片'''
    return doc.find('img').each(_replaceImg).end()

def _replaceImg(i,img):
    '''替换<img>标签的回调函数'''
    imgObj=pq(img)
    imgObj.replaceWith(r'![img]('+imgObj.attr('src')+')')

def fetchTieBaPage(url,file=None,minWords=0):
    '''抓取指定的百度贴吧帖子内容，如果指定file参数则可以输出到文件
    minWords参数指定贴子中需要过滤的最小文字长度，默认为0表示不过滤'''
    if not url:
        return
    #可以输入贴子数字编号来获取内容
    if url.isalnum():
        url='http://tieba.baidu.com/p/'+url+'?see_lz=1'
    elif 'tieba.baidu.com/p/' not in url:
        print('错误：无法识别的贴吧贴子地址！')
        return
    #如果有指定file参数，会将内容保存到文件中
    if file and isinstance(file,str):
        try:
            f=codecs.open(file,mode='wb',encoding='utf-8')
        except:
            print('错误：无法输出至指定文件！','\n')
            f=None
    elif isinstance(file,codecs.StreamReaderWriter):
        f=file
    else:
        f=None
    try:
        page=pq(url)
        doc=page.find('div.d_post_content')
    except:
        print('错误：无法获取贴子[%s]的内容！'%(url))
    #循环读取每一个楼层的文本内容
    for node in doc:
        p=pq(node)
        lenWords=len(p.text())
        parseText=parseImg(parseBr(p)).text().lstrip()
        if minWords is None or minWords<=0 or lenWords>minWords:
            print(parseText)
            if f:
                print('-'*80)
                isDel=input('按回车键保留本段文字，其它键删除本段：')
                print('='*80)
                if not isDel:
                    f.write(parseText)
                    f.write('\n')
            else:
                input('')
    #如果有下一页，则读取下一页的内容
    link=page.find('div.l_thread_info').find('a').filter(lambda i: pq(this).text() == '下一页')
    if len(link)>0:
        fetchTieBaPage('http://tieba.baidu.com%s'%(link.eq(0).attr('href')),f,minWords)
    #如果没有下一页则关闭输出的文件对象
    elif isinstance(f,codecs.StreamReaderWriter):
        f.close()

def main():
    url=''
    while not url:
        url=input('请输入百度贴吧贴子地址：')
    f=input('请输入保存的文件名：')
    print('='*80,'\n')        
    fetchTieBaPage(url,f,100)

if __name__ == '__main__':
    main()

