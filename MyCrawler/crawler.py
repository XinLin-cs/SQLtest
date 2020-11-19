import requests
from bs4 import BeautifulSoup
from urllib import request
import re
import pandas as pd

def clear_data(str):
    str = re.sub('[\n\r]','',str)
    return str

def get_item(url):
    res = request.urlopen(url)
    response = requests.get(url)
    http_status_code = response.status_code
    try:
        # 生成soup对象
        soup = BeautifulSoup(res,"html.parser")

        # 获取pid
        pid = soup.find(attrs={"id":re.compile("pid")})['id']
        pid = re.sub('pid','',pid)
        # print(pid)

        # 获取帖子详情
        title = soup.find(attrs={"id":"thread_subject"}).string
        content = soup.find(attrs={"id":"postmessage_%s"%pid}).text

        # 生成数据
        item = {"title":title,"content":content}

        # 数据清洗
        for it in item:
            item[it] = clear_data(item[it])
        # print(item)
        return item
    except:
        pass

def save_as_csv(data):
    data_df = {}
    for it in data:
        for key in it:
            if data_df.get(key) is None:
                data_df[key]=[]
            data_df[key].append(it[key])
    data_df = pd.DataFrame(data_df)
    data_df.to_csv('MyCrawler/bbsdata.csv' , encoding="utf_8_sig")

if __name__ == '__main__':
    itemlist = []
    for i in range(661000,661005):
        url = "http://cskaoyan.com/thread-%d-1-1.html"%i
        item = get_item(url)
        if not item is None:
            itemlist.append(item)
    # print(itemlist)
    save_as_csv(itemlist)