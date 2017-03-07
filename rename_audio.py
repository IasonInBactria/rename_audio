#coding:utf-8

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
            ret_html = ret.text
            # print ret_html
            xpath_tree = html.fromstring(ret_html)
            name_list = xpath_tree.xpath('//div[@class="text name"]/span[@class="font-normal"]/text()')
            for item in name_list:
                print item


if __name__ == '__main__':
    print '请输入相对网址：'
    audio_url = 'http://www.justing.com.cn/' + raw_input()
    print '请输入音频文件全路径：'
    audio_dir = raw_input()
    rename_files(audio_url, audio_dir)