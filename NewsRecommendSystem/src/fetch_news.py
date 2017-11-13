#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import os
import sys
import time
import traceback
import re
import json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from lxml import html
import requests
from requests.exceptions import Timeout, ConnectionError

from Get_newstag import get_newstag
from Get_newstag import getTags
from Get_newstag import get_SearchTags
from newsDSC import mergeAllSources
from newsSort import get_NewsRate

def echo(log_f, info):
    info = trans_coding(info, 'utf-8').encode('utf-8')
    print(info.decode('utf-8'))
    t_s = time.asctime(time.localtime(time.time()))
    t_s = trans_coding(info, 'utf-8').encode('utf-8')
    log_f.write(t_s + b'\t--\t' + info + b'\n')


def trans_coding(data, coding=''):
    if sys.version_info >= (3, 0):
        if type(data) == str:
            return data
        else:
            if coding:
                return data.decode(coding)
            else:
                if sys.platform == 'win32':
                    return data.decode('gbk')
                else:
                    return data.decode('utf-8')
    if type(data) == unicode:
        return data
    else:
        if coding:
            return data.decode(coding)
        else:
            if sys.platform == 'win32':
                return data.decode('gbk')
            else:
                return data.decode('utf-8')


def send_stop_mail(exit_code=0):
    try:
        host = 'smtp.163.com'  # 使用的SMTP服务
        port = 465  # SSL端口号，非SSL端口模式下改用25
        sender = 'record_sender@163.com'  # 发送信息的邮箱，需要在邮箱中开通SMTP服务
        pwd = 'send123456'
        receiver = '835542226@qq.com'  # 接收信息的邮箱

        stop_msg = MIMEMultipart()
        if exit_code == 1000:
            text = 'exit code 1000 , spider finish task，please start new task。'
        else:
            text = 'exit code %d , news_spider已经停止工作，请重启spider，错误原因见日志。' % exit_code
        stop_msg.attach(MIMEText(text, 'plain', 'utf-8'))
        stop_msg['subject'] = 'news_spider工作状态发送'  # 邮件标题
        stop_msg['from'] = sender
        stop_msg['to'] = receiver

        s = smtplib.SMTP_SSL(host, port)  # 使用SSL端口
        s.login(sender, pwd)  # 登陆邮箱
        s.sendmail(sender, receiver, stop_msg.as_string())  # 发送邮件
        s.quit()  # 关闭链接
        print('邮件发送成功\n')
    except:
        print(traceback.format_exc())
        print('邮件发送失败\n')


class NewsSpider:

    def __init__(self):

        # 日志文件
        self.log_f = open('news_spider.log', 'ab')

        # 各门户网站域名
        self.host_urls = {
            'fenghuang': 'news.ifeng.com',
            'tengxun': 'news.qq.com',
            'wangyi': 'news.163.com',
            'xinlang': 'news.sina.com.cn',
        }

        # 抓取链接
        self.fetch_urls = {
            'fenghuang': 'http://news.ifeng.com/hotnews/',
            'tengxun': 'http://news.qq.com/articleList/ranking/',
            'wangyi': 'http://news.163.com/rank/',
            'xinlang': 'http://news.sina.com.cn/hotnews/',
        }

        # 爬虫所用UA设置，尽量使用主流UA
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        ]

        # 页面xpath配置，用于从页面获取信息
        self.xpaths = {
            'fenghuang': {
                '资讯': '//div[@id="c01"]/table/tr',
                '军事': '//div[@id="c03"]/table/tr',
                '体育': '//div[@id="c05"]/table/tr',
                '娱乐': '//div[@id="c09"]/table/tr',
            },
            'tengxun': {
                '资讯': '//div[@id="news"]/div[2]/div/ul[1]/li',
                '时政': '//div[@id="politics"]/div[2]/div/ul[1]/li',
                '国际': '//div[@id="international"]/div[2]/div/ul[1]/li',
                '财经': '//div[@id="finance"]/div[2]/div/ul[1]/li',
                '体育': '//div[@id="sports"]/div[2]/div/ul[1]/li',
                '娱乐': '//div[@id="ent"]/div[2]/div/ul[1]/li',
                '时尚': '//div[@id="fashion"]/div[2]/div/ul[1]/li',
                '汽车': '//div[@id="auto"]/div[2]/div/ul[1]/li',
                '房产': '//div[@id="house"]/div[2]/div/ul[1]/li',
                '游戏': '//div[@id="games"]/div[2]/div/ul[1]/li',
                '社会': '//div[@id="society"]/div[2]/div/ul[1]/li',
                '教育': '//div[@id="edu"]/div[2]/div/ul[1]/li',
                '旅游': '//div[@id="ly"]/div[2]/div/ul[1]/li',
            },
            'wangyi': {
                '资讯': '//div[@class="area-half left"][2]/div[@class="tabBox"]/div',
                '娱乐': '//div[@class="area-half left"][3]/div[@class="tabBox"]/div',
                '体育': '//div[@class="area-half left"][4]/div[@class="tabBox"]/div',
                '财经': '//div[@class="area-half left"][5]/div[@class="tabBox"]/div',
                '科技': '//div[@class="area-half left"][6]/div[@class="tabBox"]/div',
                '汽车': '//div[@class="area-half left"][7]/div[@class="tabBox"]/div',
                '时尚': '//div[@class="area-half left"][8]/div[@class="tabBox"]/div',
                '房产': '//div[@class="area-half left"][9]/div[@class="tabBox"]/div',
                '教育': '//div[@class="area-half left"][13]/div[@class="tabBox"]/div',
            },
            'xinlang': {
                '资讯': '//div[@id="Con21"]//table//script[@src]',
                '国际': '//div[@id="Con31"]//table//script[@src]',
                '社会': '//div[@id="Con41"]//table//script[@src]',
                '体育': '//div[@id="Con51"]//table//script[@src]',
                '财经': '//div[@id="Con71"]//table//script[@src]',
                '娱乐': '//div[@id="Con81"]//table//script[@src]',
                '科技': '//div[@id="Con61"]//table//script[@src]',
                '军事': '//div[@id="Con91"]//table//script[@src]',
            },
        }

        # 爬虫信息记录参数
        self.exit_code = 0
        self.news_count = 0

        # 存储路径配置
        if sys.platform == 'win32':
            # self.to_dir = u'/get_news_file/'
            self.to_dir = u'get_news_file/'
        else:
            # self.to_dir = u'/home/mengxiaoji/get_news_file/'
            self.to_dir = u'get_news_file/'

        if not os.path.exists(self.to_dir):
            os.makedirs(self.to_dir)

    def fetch_fenghuang(self):
        echo(self.log_f, '开始爬取凤凰网')
        resp = self.make_request(url=self.fetch_urls['fenghuang'], host=self.host_urls['fenghuang'])
        page_html = html.fromstring(resp.content)
        news_dict = {}
        for t_kind, t_xpath in self.xpaths['fenghuang'].items():
            echo(self.log_f, '获取 %s 分类新闻' % t_kind)
            t_table = page_html.xpath(t_xpath)
            for i in range(1, len(t_table)):
                news_a = t_table[i].find('./td[2]/h3/a')
                news_url = news_a.get('href')
                news_title = news_a.text.strip()
                news_weight = int(t_table[i].find('./td[3]').text)
                news_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                if news_url not in news_dict:
                    news_dict[news_url] = '%s<div/>%s<div/>%s<div/>%d<div/>%s\n' % (t_kind, news_url, news_title, news_weight, news_date)
        echo(self.log_f, '爬取凤凰网完毕，储存于 fenghuang.rec 内')
        news_lines = news_dict.values()
        with open(os.path.join(self.to_dir, 'fenghuang.rec'), 'wb') as fenghuang_f:
            fenghuang_f.writelines([trans_coding(line, 'utf-8').encode('utf-8') for line in news_lines])
            self.news_count += len(news_lines)

    def fetch_tengxun(self):
        echo(self.log_f, '开始爬取腾讯网')
        resp = self.make_request(url=self.fetch_urls['tengxun'], host=self.host_urls['tengxun'])
        page_html = html.fromstring(resp.content.decode('gbk'))
        news_dict = {}
        for t_kind, t_xpath in self.xpaths['tengxun'].items():
            echo(self.log_f, '获取 %s 分类新闻' % t_kind)
            t_ul = page_html.xpath(t_xpath)
            for i in range(len(t_ul)):
                news_a = t_ul[i].find('.//div[@class="info"]/p/a')
                news_url = news_a.get('href')
                news_title = news_a.text.strip()
                news_weight = int(re.search(u'(\d)+', t_ul[i].find('.//div[@class="info"]//span[@class="heatIndex"]').text).group())
                news_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                if news_url not in news_dict:
                    news_dict[news_url] = '%s<div/>%s<div/>%s<div/>%d<div/>%s\n' % (t_kind, news_url, news_title, news_weight, news_date)
        echo(self.log_f, '爬取腾讯网完毕，储存于 tengxun.rec 内')
        news_lines = news_dict.values()
        with open(os.path.join(self.to_dir, 'tengxun.rec'), 'wb') as tengxun_f:
            tengxun_f.writelines([trans_coding(line, 'utf-8').encode('utf-8') for line in news_lines])
            self.news_count += len(news_lines)

    def fetch_wangyi(self):
        echo(self.log_f, '开始爬取网易网')
        resp = self.make_request(url=self.fetch_urls['wangyi'], host=self.host_urls['wangyi'])
        page_html = html.fromstring(resp.content.decode('gbk'))
        news_dict = {}
        for t_kind, t_xpath in self.xpaths['wangyi'].items():
            echo(self.log_f, '获取 %s 分类新闻' % t_kind)
            divs = page_html.xpath(t_xpath)[1:3]
            for i in range(len(divs)):
                t_table = divs[i].findall('.//tr')
                for j in range(1, len(t_table)):
                    news_a = t_table[j].find('./td[1]/a')
                    news_url = news_a.get('href')
                    news_title = news_a.text.strip()
                    news_weight = int(t_table[j].find('./td[2]').text)
                    news_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                    if news_url not in news_dict:
                        news_dict[news_url] = '%s<div/>%s<div/>%s<div/>%d<div/>%s\n' % (t_kind, news_url, news_title, news_weight, news_date)
        echo(self.log_f, '爬取网易网完毕，储存于 wangyi.rec 内')
        news_lines = news_dict.values()
        with open(os.path.join(self.to_dir, 'wangyi.rec'), 'wb') as wangyi_f:
            wangyi_f.writelines([trans_coding(line, 'utf-8').encode('utf-8') for line in news_lines])
            self.news_count += len(news_lines)

    def fetch_xinlang(self):
        echo(self.log_f, '开始爬取新浪网')
        resp = self.make_request(url=self.fetch_urls['xinlang'], host=self.host_urls['xinlang'])
        page_html = html.fromstring(resp.content)
        news_dict = {}
        stop_time = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*3))
        for t_kind, t_xpath in self.xpaths['xinlang'].items():
            echo(self.log_f, '获取 %s 分类新闻' % t_kind)
            t_fetch_url = page_html.xpath(t_xpath)[0].get('src')
            t_fetch_url = re.sub(r'top_show_num=(\d+)&', 'top_show_num=50&', t_fetch_url)
            t_fetch_host = re.search(r'http://([^/]+)/', t_fetch_url).group(1)
            t_var = re.search(r'&js_var=(.+_)', t_fetch_url).group(1)
            re_t = 0
            while True:
                try:
                    news_resp = self.make_request(url=t_fetch_url, host=t_fetch_host)
                    time.sleep(1)
                    news_list = json.loads(re.search(r'var %s = ({.+});' % t_var, news_resp.content.decode('utf-8')).group(1))['data']
                    break
                except:
                    re_t += 1
                    if re_t > 5:
                        self.exit_code = 4
                        raise Exception('no content error')
            for news_info in news_list:
                if stop_time <= news_info['create_date']:
                    news_url = news_info['url'].encode('utf-8')
                    news_title = news_info['title'].strip()
                    news_weight = int(re.sub(u',', '', news_info['top_num']))
                    news_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                    if news_url not in news_dict:
                        news_dict[news_url] = '%s<div/>%s<div/>%s<div/>%d<div/>%s\n' % (t_kind, news_url, news_title, news_weight, news_date)
        echo(self.log_f, '爬取新浪网完毕，储存于 xinlang.rec 内')
        news_lines = news_dict.values()
        with open(os.path.join(self.to_dir, 'xinlang.rec'), 'wb') as xinlang_f:
            xinlang_f.writelines([trans_coding(line, 'utf-8').encode('utf-8') for line in news_lines])
            self.news_count += len(news_lines)

    def start(self):
        try:
            self.fetch_fenghuang()
            self.fetch_tengxun()
            self.fetch_wangyi()
            self.fetch_xinlang()
            echo(self.log_f, '共获取新闻总数 %d' % self.news_count)

            ######
            # fenghuang.rec
            # tengxun.rec
            # wangyi.rec
            # xinlang.rec
            # 要打印信息请用echo(self.log_f, '')
            ######
            path = 'D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt'
            fr1 = open("fenghuang.rec",encoding='utf-8')
            fr2 = open("tengxun.rec",encoding='utf-8')
            fr3 = open("wangyi.rec",encoding='utf-8')
            fr4 = open("xinlang.rec",encoding='utf-8')
            source1 = {}
            source2 = {}
            source3 = {}
            source4 = {}
            allInfo = {}
            for line in fr1.readlines():
                info = line.split('<div/>')
                kind = info[0]
                id = info[1]
                title = info[2]
                num = int(info[3])
                time = info[4]
                data = time.split(' ')[0]
                tags = getTags(title, path)
                rate = get_NewsRate(num, time)
                source1[id] = [tags,num]
                allInfo[id] = {'title':title,'url':id,'kind':kind,'hot_rate':rate,'data':data}            
            for line in fr2.readlines():
                info = line.split('<div/>')
                kind = info[0]
                id = info[1]
                title = info[2]
                num = int(info[3])
                time = info[4]
                data = time.split(' ')[0]
                tags = getTags(title, path)
                rate = get_NewsRate(num, time)
                source2[id] = [tags,num]
                allInfo[id] = {'title':title,'url':id,'kind':kind,'hot_rate':rate,'data':data}
            for line in fr3.readlines():
                info = line.split('<div/>')
                kind = info[0]
                id = info[1]
                title = info[2]
                num = int(info[3])
                time = info[4]
                data = time.split(' ')[0]
                tags = getTags(title, path)
                rate = get_NewsRate(num, time)
                source3[id] = [tags,num]
                allInfo[id] = {'title':title,'url':id,'kind':kind,'hot_rate':rate,'data':data}
            for line in fr4.readlines():
                info = line.split('<div/>')
                kind = info[0]
                id = info[1]
                title = info[2]
                num = int(info[3])
                time = info[4]
                data = time.split(' ')[0]
                tags = getTags(title, path)
                rate = get_NewsRate(num, time)
                source4[id] = [tags,num]
                allInfo[id] = {'title':title,'url':id,'kind':kind,'hot_rate':rate,'data':data}
            source = [source1,source2,source3,source4]
            # 汇总新闻url数组
            allNews = mergeAllSources(source,path)
            
            # 生成三个字典:1.mergedTable; 2.newsLimitedTags; 3.newsTags;
            mergedTable = {}
            for news in allInfo:
                if news in allNews:
                    mergedTable[news] = allInfo[news]
            
            newsTitle = {}
            for news,info in allInfo.items():
                newsTitle[news] = info['title']
            
            newsLimitedTags = get_SearchTags(newsTitle)
            newsSearchTags = get_newstag(newsTitle, path)

            self.exit_code = 1000
        except:
            echo(self.log_f, traceback.format_exc())
            self.exit_code = 5

        self.log_f.close()

    def make_request(self, url, host):
        header = {
            'User-Agent': self.user_agents[0],
            'Host': host,
        }

        re_t = 0
        while True:
            try:
                echo(self.log_f, 'start to fetch %s' % url)
                resp = requests.get(url=url, headers=header, timeout=15)
                if resp.content:
                    return resp
                re_t += 1
                if re_t == 6:
                    echo(self.log_f, 'Forbidden, long sleep 10min')
                    time.sleep(600)
                if re_t > 10:
                    self.exit_code = 3
                    raise Exception('Forbidden error')
                echo(self.log_f, 're fetch %s %d times' % (url, re_t))
            except (Timeout, ConnectionError):
                re_t += 1
                if re_t == 6:
                    echo(self.log_f, 'Forbidden, long sleep 10min')
                    time.sleep(600)
                if re_t > 10:
                    self.exit_code = 2
                    raise Exception('Connect error')
                echo(self.log_f, 're fetch %s %d times' % (url, re_t))


if __name__ == '__main__':
    try:
        spider = NewsSpider()
        spider.start()
        # if spider.exit_code != 1:
        #     send_stop_mail(spider.exit_code)
    except:
        echo(open('news_spider.log', 'ab'), traceback.format_exc())
        # send_stop_mail(4)

    print('执行完毕')
    
    
