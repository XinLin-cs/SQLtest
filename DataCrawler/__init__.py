from DataCrawler import crawler

# 主函数
if __name__ == '__main__':
    # start_id, terminal_id = 660000, 660010
    start_id, terminal_id = 660000, 661000
    # itemlist = work_by_linear(start_id , terminal_id)
    itemlist = crawler.work_by_threads(start_id, terminal_id)
    crawler.save_as_csv(itemlist)
