# python3.5
# urlScan.py
# Author：FrankHacker


import requests
import re
import os
import urllib3
import time


def url_is_correct():
    '''
    使用requests.get方法判断url是否正确,并返回url
    :return:
    '''
    try:
        url = input("请输入被测url:")
        # url = "http://10.70.18.47:8080" 这是我内网环境的测试地址
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'connection': 'close'}
        requests.get(url, headers=headers)
        return url
    except:
        print('请输入正确的url!!!')
        # exit(-1)   #如果url是固定写入的，那么必须添加此句，否则会一直循环
    return url_is_correct()


url = url_is_correct()  # 将验证为正确的url地址赋值给url


def url_protocol(url):
    '''
    获取输入的url地址的协议，是http、https等
    '''
    print('该站使用的协议是：' + re.findall(r'.*(?=://)', url)[0])
    return re.findall(r'.*(?=://)', url)[0]


urlprotocol = url_protocol(url)


def same_url(url):
    '''
    处理用户输入的url，并为后续判断是否为一个站点的url做准备，爬取的时候不能爬到其它站，那么爬取将无止境
    :return: sameurl
    '''
    # 将完整的url中的http://删除
    url = url.replace(urlprotocol + '://', '')
    protocol, host, a = urllib3.get_host(url)
    '''
    #判断删除http://之后的url有没有www，如果没有就加上‘www.’，但不存储，
    #只是为了同化所有将要处理的url，都有了‘www.’之后，
    #就可以找以‘www.’开始的到第一个‘/’结束中的所有字符串作为该站的主域名
    if re.findall(r'^www',url) == []:
        sameurl = 'www.' + url
        if sameurl.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
        else:
            sameurl = sameurl + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    else:
        if url.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', url)[0]
        else:
            sameurl = url + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    print('同站域名地址：' + sameurl)
    '''
    print('同站域名地址：' + host)
    return host


domain_url = same_url(url)

'''
处理url的类，对已访问过的和未访问过的进行记录，待后续使用
'''


class linkQuence:
    def __init__(self):
        self.visited = []  # 已访问过的url初始化列表
        self.unvisited = []  # 未访问过的url初始化列表

    def getVisitedUrl(self):  # 获取已访问过的url
        return self.visited

    def getUnvisitedUrl(self):  # 获取未访问过的url
        return self.unvisited

    def addVisitedUrl(self, url):  # 添加已访问过的url
        return self.visited.append(url)

    def addUnvisitedUrl(self, url):  # 添加未访问过的url
        if url != '' and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0, url)

    def removeVisited(self, url):
        return self.visited.remove(url)

    def popUnvisitedUrl(self):  # 从未访问过的url中取出一个url
        try:  # pop动作会报错终止操作，所以需要使用try进行异常处理
            return self.unvisited.pop()
        except:
            return None

    def unvisitedUrlEmpty(self):  # 判断未访问过列表是不是为空
        return len(self.unvisited) == 0


class Spider():
    '''
    真正的爬取程序
    '''

    def __init__(self, url):
        self.linkQuence = linkQuence()  # 引入linkQuence类
        self.linkQuence.addUnvisitedUrl(url)  # 并将需要爬取的url添加进linkQuence对列中
        self.current_deepth = 1  # 设置爬取的深度
        '''
        这里需要注意:
        爬取分为：***先深度后广度***和***先广度和后深度***
        1、如果是先深度后广度，那么给定一个url，然后从其页面中的任意一个可用链接进行深度爬取，很可能无限至循环下去
        （在处理不当的时候，但一般情况下大家都会处理的很好，无非是判断哪些url是已经爬取过的，哪些是新爬取到的url）
        2、如果是先广度后深度，就是将一个url页面中的所有链接进行爬取，然后分类处理过滤
        （在这种处理不当的时候也会出现无限循环的可能，但一般情况下大家都会处理的很好，无非是判断哪些url是已经爬取过的，哪些是新爬取到的url）
        '''

    def getPageLinks(self, url):
        '''
        获取页面中的所有链接
        '''
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        pageSource = requests.get(url, headers=headers).text
        pageLinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')', pageSource)
        for l in pageLinks:
            print(url + '该页面的源码链接有：' + l)
        return pageLinks

    def processUrl(self, url):
        '''
        判断正确的链接及处理相对路径为正确的完整url
        :return:
        '''
        true_url = []
        for l in self.getPageLinks(url):  # 从页面中找出有效的url
            if re.findall(r'/', l):
                if re.findall(r':', l):
                    true_url.append(l)
                elif re.findall(r'^//', l):  # 因部分网站内容用//:+地址表示需要添加对应协议的地址，所以需要增加此项过滤
                    true_url.append(urlprotocol + ':' + l)
                else:
                    true_url.append(urlprotocol + '://' + domain_url + l)
        for l in true_url:
            print(url + '该url页面源码中，有效url：' + l)
        return true_url

    def sameTargetUrl(self, url):
        '''
        判断是否为同一站点链接，防止爬出站外，然后导致无限尝试爬取
        '''
        same_target_url = []
        for l in self.processUrl(url):  # 从有效url中找出属于同一域名下的url
            if re.findall(domain_url, l):
                same_target_url.append(l)
        for l in same_target_url:
            print(url + '该url页面源码中属于同一域的url有：' + l)
        return same_target_url

    def unrepectUrl(self, url):
        '''
        删除重复url
        '''
        unrepect_url = []
        for l in self.sameTargetUrl(url):  # 对该url页面源码中属于同一域的url进行去重
            if l not in unrepect_url:
                unrepect_url.append(l)
        for l in unrepect_url:
            print(url + '该url下不重复的url有------：' + l)

        return unrepect_url

    def crawler(self, crawl_deepth=1):
        '''
        正式的爬取，并依据深度进行爬取层级控制
        '''
        while self.current_deepth <= crawl_deepth:  # 判断目前爬取深度
            while not self.linkQuence.unvisitedUrlEmpty():  # 如果未访问列表不是空
                visitedUrl = self.linkQuence.popUnvisitedUrl()  # 从未访问列表取出一个url
                # print(visitedUrl)
                if visitedUrl is None or visitedUrl == '':  # 判断取出的连接是否为空
                    continue
                # self.getPageLinks(visitedUrl)
                links = self.unrepectUrl(visitedUrl)  # 找出该url页面上包含的不重复的url
                if visitedUrl not in self.linkQuence.getVisitedUrl():
                    print('把连接加入已访问列表之前的已访问列表内容：', self.linkQuence.getVisitedUrl())
                    self.linkQuence.addVisitedUrl(visitedUrl)  # 已访问过的url加入已访问列表
                    print('把连接加入已访问列表之后的已访问列表内容：', self.linkQuence.getVisitedUrl())
                for link in links:
                    print('link:', link)
                    print('把连接加入未访问列表之前的未访问列表内容：', self.linkQuence.getUnvisitedUrl())
                    self.linkQuence.addUnvisitedUrl(link)  # 把取出的未访问连接放入未访问列表
                    print('把连接加入未访问列表之后的未访问列表内容：', self.linkQuence.getUnvisitedUrl())

            self.current_deepth += 1

        host = same_url(url)  # 再次确定域名，用于创建相关存储文件路径
        target_url = self.linkQuence.visited
        projectpath = os.path.abspath('.') + '\\projects\\' + host
        if not os.path.exists(projectpath):
            os.makedirs(projectpath)
        target_num = len(self.linkQuence.visited)
        fobj1 = open(projectpath + '\\' + host + '.txt', 'w')  # 在本目录下创建一个txt文件，里面存储最终得到的内容
        for i in range(target_num):
            # noinspection PyTypeChecker
            print(target_url[i], file=fobj1)
        fobj1.close()

        return self.linkQuence.visited


if __name__ == '__main__':
    spider = Spider(url)
    spider.crawler(1)
