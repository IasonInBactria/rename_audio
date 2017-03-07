# coding:utf-8

import os
import requests
from lxml import html


def rename_files(url, path):
    audio_url = url
    if not os.path.isdir(path):
        print '路径有误，请检查！'
    else:
        header = {}
        header['Host'] = 'www.justing.com.cn'
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        header['Referer'] = 'http://www.justing.com.cn/'

        # 模拟登录
        ret = requests.get(audio_url, headers=header)
        if ret.status_code != 200:
            print '获取信息失败！状态码%d，%s' % (ret.status_code, str(ret.reason))
            return False
        else:
            name_list = []
            ret_html = ret.text
            print ret_html
            xpath_tree = html.fromstring(ret_html)
            raw_list = xpath_tree.xpath('//a[@class="opt download-btn"]/@href')
            # for item in raw_list:
                # name_list.append(item.encode('utf-8').split('attrname=')[1])
                # print item

            # 遍历目录
            file_list = os.listdir(path)
            count = 1
            for item in name_list:
                item_content = item.split('\n')[1].encode('utf-8')
                print item_content
                # if item_content in file_list:
                #     new_item = '%02d.%s' % (count, item_content)
                #     new_name = os.path.join(path, new_item)
                #     os.rename(os.path.join(path, item_content), new_name)
                #     count += 1


if __name__ == '__main__':
    print '请输入相对网址：'
    audio_url = 'http://www.justing.com.cn/' + raw_input()
    print '请输入音频文件全路径：'
    audio_dir = raw_input()
    rename_files(audio_url, audio_dir)