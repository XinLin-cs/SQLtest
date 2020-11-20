import requests
from bs4 import BeautifulSoup
from urllib import request
import re
import pandas as pd
import string
from queue import Queue
import _thread
import time

def clear_data(str):
    str = re.sub('[\n\r]','',str)
    return str

def get_item(url):
    try:
        res = request.urlopen(url)
        response = requests.get(url)
        http_status_code = response.status_code
        # 生成soup对象
        soup = BeautifulSoup(res,"html.parser")

        # 获取pid
        pid = soup.find(attrs={"id":re.compile("pid")})['id']
        pid = re.sub('pid','',pid)
        # print(pid)

        # 获取帖子详情
        # 发表时间
        post_time = soup.find(attrs={"id":"authorposton%s"%pid}).string
        # 标题及内容
        title = soup.find(attrs={"id":"thread_subject"}).string
        content = soup.find(attrs={"id":"postmessage_%s"%pid}).text
        # 查看和回复数
        interact_div = soup.find(attrs={"class":"hm ptn"})
        interact_list = re.findall('\d+', interact_div.text)
        watches = interact_list[0]
        replies = interact_list[1]
        # 收藏 赞 踩
        favorites = soup.find(attrs={"id":"favoritenumber"}).string
        likes = soup.find(attrs={"id":"recommendv_add"}).string
        dislikes = soup.find(attrs={"id":"recommendv_subtract"}).string
        # 附件
        additions_flag = "0"
        additions = soup.find(attrs={"class":"attach_nopermission attach_tips"})
        if not additions is None:
            additions_flag = "1"
        # 作者信息
        writer_name = soup.find(attrs={"class":"authi"}).text
        writer_year = soup.find(attrs={"class":"pil cl"}).contents[2].string
        writer_targetschool = soup.find(attrs={"class":"pil cl"}).contents[5].string
        writer_school = soup.find(attrs={"class":"pil cl"}).contents[8].string
        # 生成数据
        item = {
            "url":url,
            "post_time":post_time,
            "title":title,"content":content,
            "watches":watches,"replies":replies,
            "favorites":favorites,"likes":likes,"dislikes":dislikes,
            "additions":additions_flag,
            "writer_name":writer_name,
            "writer_year":writer_year,
            "writer_school":writer_school,
            "writer_targetschool":writer_targetschool,
            }

        # 数据清洗
        # for it in item:
        #     if type(item[it]) == string:
        #         item[it] = clear_data(item[it])
        # print(item)
        return item
    except BaseException as e:
        # print("ERROR: When request" , url , "WITH:", e)
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

# 线性访问
def work_by_linear(start_id , terminal_id):
    itemlist = []
    for i in range(start_id,terminal_id):
        url = "http://cskaoyan.com/thread-%d-1-1.html"%i
        item = get_item(url)
        if not item is None:
            itemlist.append(item)
        rate = 100.0 * (i - start_id + 1) / (terminal_id - start_id)
        print("%.1f" % rate , "%")
    return itemlist

# 多线程爬虫
thq = Queue(maxsize=0)
cnt = 0

def get_item_thread(url,a,b):
    global thq , cnt
    item = get_item(url)
    cnt += 1
    thq.put(item)

def rollingbar_start(tot,b,c):
    global cnt
    bar = 0
    while cnt<tot:
        time.sleep(0.1)
        if cnt>bar:
            bar = cnt
            rate = 100.0 * bar / tot
            print("%.1f" % rate , "%")

def work_by_thread(start_id , terminal_id):
    global thq , cnt
    tot = terminal_id - start_id
    
    _thread.start_new_thread( rollingbar_start , (tot, 1, 1) )
    for i in range(start_id,terminal_id):
        url = "http://cskaoyan.com/thread-%d-1-1.html"%i
        _thread.start_new_thread( get_item_thread, (url, 1, 1) )
        time.sleep(0.1)
    
    while cnt<tot:
        time.sleep(1)
        
    itemlist = []
    while not thq.empty():
        item = thq.get()
        if not item is None:
            itemlist.append(item)
    return itemlist

# 主函数
if __name__ == '__main__':
    start_id , terminal_id = 660000 , 660500
    # itemlist = work_by_linear(start_id , terminal_id)
    itemlist = work_by_thread(start_id , terminal_id)
    save_as_csv(itemlist)