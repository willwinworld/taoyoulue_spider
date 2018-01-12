from page_get.silver.news_content import get_news_content
from config.conf import NEWS_CONTENT_URL
from bs4 import BeautifulSoup
from lxml import html
import re
import os
from page_parse import qiniu


def parse_news_content(article_id):

    res = get_news_content(article_id)
    print("article_id:", article_id)
    # collect div
    soup = BeautifulSoup(res.text, 'html.parser')
    res_div = soup.find('div', class_='detail-content')
    # print(res_div)
    # judge img
    etree = html.fromstring(res.text)
    el = etree.xpath("//div[@class='detail-content']//span//img")
    # img ture save qiniu
    if el:
        img_src = el[0].attrib['src']
        # save img to qiniu
        img_list = re.split('/', img_src)
        key = img_list[-1]
        save2qiniu(key, img_src)
        # replace img path
        src = res_div.find('img')
        print(dir(src))
        src['src'] = os.path.join("http://cdn.re-media.cn", key)
    # save div
    print(str(res_div))
    return str(res_div)

if __name__ == "__main__":
    parse_news_content(32702)