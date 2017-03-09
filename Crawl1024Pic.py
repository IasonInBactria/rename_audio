# coding:utf-8
import requests
from lxml import html
import os


proxy = {"http":"http://127.0.0.1:1080", "https": "https://127.0.0.1:1080"}
header = {'Host': 't66y.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                                            'Chrome/56.0.2924.87 Safari/537.36'}
ret = requests.get('http://t66y.com/htm_data/16/1703/2284010.html', proxies=proxy, verify=False)
if ret.status_code != 200:
    print '获取xsrf信息失败！状态码%d，%s' % (ret.status_code, str(ret.reason))
else:
    ret.encoding = ret.apparent_encoding
    ret_html = ret.text
    # print ret_html.encode('utf-8')
    xpath_tree = html.fromstring(ret_html)
    image_list = xpath_tree.xpath('//input[@type="image"]/@src')
    # XPath的序号是从1开始的！！！！
    title = xpath_tree.xpath('//div[@id="main"]/div[@class="t"]/table/tr/td[1]/text()[2]')[0]
    cur_dir = os.path.join(os.path.curdir, title)
    os.mkdir(cur_dir)
    count = 0
    for item in image_list:
        ret = requests.get(item)
        if ret.status_code == 200:
            cur_file_name = '%d.jpg' % count
            with open(os.path.join(cur_dir, cur_file_name), 'wb') as f:
                f.write(ret.content)
                f.close()
                count += 1
