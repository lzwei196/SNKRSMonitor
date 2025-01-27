#!/usr/bin/python3
# coding:utf-8
import sys

import urllib3
import json
import time
from datetime import datetime
import traceback
from collections import deque
import os
import requests
from webhook import notifyDisc

try:
    import winsound
except ImportError:
    pass
import platform

from enum import Enum

urllib3.disable_warnings()

ip_port=None
auth=None
nike_US_baseurl='https://www.nike.com/launch/t/'
nike_CHINA_baseurl='https://www.nike.com/cn/launch/t/'
nike_baseurl='https.googlsadaf'


try:
    ip_port = sys.argv[2] #hype9049143:pwd994143
    auth = sys.argv[3] #12.164.246.247:35000
    print('running on proxy ' + ip_port)
except:
    print('not proxy configuration detected, running on server ip')



def formatTimeStr(str1):
    return str1[0:10] + " " + str1[11:19]


def getTime(str1):
    return time.mktime(time.strptime(formatTimeStr(str1), "%Y-%m-%d %H:%M:%S"))


def getLocalTimeStr(str1):
    tm = getTime(str1)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(tm + 28800)))


def addsepline():
    print("-----------------------------------------------------------------------------------------------")


def addseptag():
    print("##################################################################")


# copyright


addsepline()
print("SNKRSMonitor 2.2")
addsepline()


# URL


class RegionURL(Enum):
    cn = "&country=CN&language=zh-Hans"
    us = "&country=US&language=en"
    jp = "&country=JP&language=ja"


class OrderBy(Enum):
    published = "&orderBy=published"
    updated = "&orderBy=lastUpdated"


url = "https://api.nike.com/snkrs/content/v1/?"

areaCode = input("请选择市场区域(1:美国,2:日本,3:中国):")
#areaCode = sys.argv[1]
if areaCode == "1":
    url += RegionURL.us.value
    nike_baseurl = nike_US_baseurl
    print('美国')
elif areaCode == "2":
    url += RegionURL.jp.value3
    raise ValueError('baseurl not implemented!!!!!.')
    print('日本')
else:
    url += RegionURL.cn.value
    nike_baseurl = nike_CHINA_baseurl
    print('中国')

print(nike_baseurl)

# user setup
addsepline()
# keyword = "off white "
# #frequency = 3
# warningTime = 5
inputfreq = input("请设定接口访问频率(秒)，访问频率过快可能会导致服务器异常，默认是3，最小是1:")
try:
   frequency = int(inputfreq)
except:
     print("输入出错，按照默认频率请求")
# if frequency <= 0:
#      frequency = 3
# warning = input("请设定发现新款过后报警次数，默认是5，最小是1:")
# try:
#     warningTime = int(warning)
# except:
#     print("输入出错，按照默认次数报警")
warningTime = 5
keyword = input("设定库存监控关键词,多个关键词用空格区分(eg:off white):")
# print("服务器实时请求接口中(" + str(frequency) + "秒每次)...")
#addseptag()

# Sneaker data
print("正在抓取最新发布球鞋数据...")
sneakers = []  # 球鞋缓存
ludict = {}  #
totalCount = 1000000


# print sneaker data


def printSneaker(data, other=None):
    str1 = data["name"] + " " + data["title"]
    try:
        if data["product"]["colorDescription"]:
            str1 += ("[" + data["product"]["colorDescription"] + "]")
        if data["product"]["merchStatus"]:
            str1 += ("[" + data["product"]["merchStatus"] + "]")
    except:
        pass
    if data["restricted"]:
        str1 += "[受限]"
    #notifyDisc(str1)
    notifyDisc(nike_CHINA_baseurl + data['seoSlug'])
    print(other, str1)


def printSneakerDetail(data):
    dict1 = {
        "LEO": "LEO(限量)",
        "DAN": "DAN(抽签)",
    }
    product = data["product"]
    try:
        name = product["title"] + "[" + product["colorDescription"] + "]"
        if data["restricted"]:
            name += "[受限]"
        price = "价格:" + str(product["price"]["msrp"])
        publicType = "发售方式:正常"
        if product["publishType"] == "LAUNCH":
            engine = product["selectionEngine"]
            publicType = "发售方式:" + dict1[engine]
        launchInfo = "不可购买"
        if product["merchStatus"] == "ACTIVE" and product["available"] and "stopSellDate" not in product.keys():
            launchInfo = "发售时间:" + getLocalTimeStr(product["startSellDate"])
        ###May need to change the baseUrl depending on the selection choice
        notifyDisc(nike_CHINA_baseurl + data['seoSlug'])
        data = 'name: %s \n \
                name: % s \n \
                name: % s \n \
                name: % s ' % (name, price, publicType, launchInfo)
        #notifyDisc(data)
        print(name)
        print(price)
        print(publicType)
        print(launchInfo)
    except Exception as e:
        print(str(e))


# request sneaker
def requestSneakers(order, offset):
    global totalCount
    requrl = url + "&offset=" + str(offset) + order
    print(requrl)
    http = None

    if ip_port is not None:
        default_headers = urllib3.make_headers(proxy_basic_auth=auth)
        http = urllib3.ProxyManager('http://@%s' % ip_port, proxy_headers=default_headers)
    else:
        http = urllib3.PoolManager()

    r = http.request("GET", requrl)
    time.sleep(0.4)
    shoes = []
    try:
        json_data = json.loads(r.data)
        if len(sneakers) >= totalCount:
            return []
        totalCount = json_data["totalRecords"]
        for data in json_data["threads"]:
            shoes.append(data["id"])
            ludict[data["id"]] = getTime(data["lastUpdatedDate"])
            #comment this out
            print(data)
            if offset == 0:
                printSneaker(data, other=requrl)
        return shoes
    except:
        print(requrl)
        print("\r访问服务器失败，3秒后重试")
        time.sleep(3)
        return requestSneakers(order, offset)


#for num in range(0, 10000):
#    k = num * 50
#    snkrs = requestSneakers(OrderBy.published.value, k)
#    if len(snkrs) == 0:
#        print("数据请求完毕,一共获取到", str(len(sneakers)), "条数据(只显示前50条)...")
#        break
#    sneakers.extend(snkrs)

# refresh request
# def sneakerAvailable(snkdata):
#    if data["restricted"]:
#        return false
#    product = data["product"]
#    if [r]

"""
def warning_hints(tip_text):
    sys_str = platform.system()
    if sys_str == "Windows":
        winsound.Beep(2600, 1000)
        print(tip_text)
    elif sys_str == "Linux":
        os.system('say ' + tip_text)
        print(tip_text)
    else:
        os.system('say ' + tip_text)
        print(tip_text)
"""

def timer(n):
    while True:
        try:
            http=None
            if ip_port is not None:
                default_headers = urllib3.make_headers(proxy_basic_auth=auth)
                http = urllib3.ProxyManager('http://@%s' % ip_port, proxy_headers=default_headers)
            else:
                http = urllib3.PoolManager()
            requesturl = url + OrderBy.published.value + "&offset=0"
            print(requesturl)
            r = http.request("GET", requesturl)
            json_data = json.loads(r.data)
            datas = json_data["threads"]
          #  with open('data.txt') as json_file:
               # sneakerDatas = json.load(json_file)
           # with open('data.txt', 'w') as outfile:
               # json.dump(datas, outfile)
            with open('dataList.txt') as json_file:
                sneakerDatas = json.load(json_file)

        except Exception as e:
            print(str(e))
            print("\r请求失败", flush=True)
            timer(n)
            break

        for data in datas:
            sneakerid = data["id"]
            t_last_update_date = data["lastUpdatedDate"]
            if sneakerid not in sneakerDatas:
              #  sneakers.append(sneakerid)
                sneakerDatas.append(sneakerid)
                ludict[data["id"]] = getTime(t_last_update_date)
                print("\r", "发现新款  更新时间:", getLocalTimeStr(t_last_update_date))
                printSneakerDetail(data)
                addseptag()
            with open('dataList.txt', 'w') as outfile:
                json.dump(sneakerDatas, outfile)
                """
            else:
                if getTime(t_last_update_date) > ludict[sneakerid]:
                    ludict[sneakerid] = getTime(t_last_update_date)
                    product = data["product"]
                    print("\r", getLocalTimeStr(t_last_update_date), end=" ")
                    t_str = "售罄"
                    if product["merchStatus"] == "ACTIVE":
                        if product["available"]:
                            t_str = "库存更新("
                            for sku in product["skus"]:
                                if sku["available"]:
                                    t_str += (sku["localizedSize"] + ",")
                                    t_str = t_str[:-1]
                                    t_str += ")"
                    print(t_str, end=" ")
                    printSneaker(data)
                    seostr = data["seoSlug"]
                    findstrs = keyword.split(" ")
                    for key in findstrs:
                        if seostr.find(key) != -1:
                            printSneakerDetail(data)
                            addseptag()
                            i = warningTime

            print("\r" + time.strftime("time :%Y-%m-%d %H:%M:%S", time.localtime(time.time())), end=" ")
            """
        time.sleep(n)


timer(10)
# SNKRSMonitor
