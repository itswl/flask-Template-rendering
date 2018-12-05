# coding:utf-8
#封装HTTP请求类
#发送http请求的两种方式

#urllib
#requests

#from urllib import request
import requests
class HTTP:  #class HTTP(object):有无都无所谓

    #或者使用静态方法，与上面一模一样
    @staticmethod
    def get(url,return_json=True):

        r = requests.get(url)

        if r.status_code != 200:
            return {} if return_json else ''      #特例情况
        return r.json() if return_json else r.text   #正常返回

#爬虫  scrapy  或 requests +beautiful soap 