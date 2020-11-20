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
        # 标题及内容
        title = soup.find(attrs={"id":"thread_subject"}).string
        content = soup.find(attrs={"id":"postmessage_%s"%pid}).text
        # 发表时间
        post_time = soup.find(attrs={"id":"authorposton%s"%pid}).string
        # 查看和回复统计
        interact_div = soup.find(attrs={"class":"hm ptn"})
        interact_list = re.findall('\d+', interact_div.text)
        watches = interact_list[0]
        replies = interact_list[1]

        # 生成数据
        item = {"url":url,"post_time":post_time,"title":title,"content":content,
        "watches":watches,"replies":replies}

        # 数据清洗
        for it in item:
            item[it] = clear_data(item[it])
        # print(item)
        return item
    except BaseException as e:
        print("ERROR: When request" , url , "WITH:", e)
        return None

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
    start_id , terminal_id = 661000 , 661010
    itemlist = []
    for i in range(start_id,terminal_id):
        url = "http://cskaoyan.com/thread-%d-1-1.html"%i
        item = get_item(url)
        if not item is None:
            itemlist.append(item)
        rate = 100.0 * (i - start_id + 1) / (terminal_id - start_id)
        print("%.1f" % rate , "%")
    # print(itemlist)
    save_as_csv(itemlist)