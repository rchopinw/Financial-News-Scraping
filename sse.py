# Arthor: B.X. Weinstein Xiao
# Contact: rchopin@outlook.com, bangxi_xiao@brown,edu

import requests
import numpy as np
import json
from random import choice
import pdfminer.high_level as ph


class SSE(object):
    def __init__(self):
        self.ua_library = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
              'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
              'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
              'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
              'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36']
        self.fn = 'cache_requests_sse.pdf'  # filename of cache
        self.rc = ['extSECURITY_CODE', 'extGSJC', 'createTime', 'extWTFL', 'docTitle', 'docURL', 'unique_id']  # rc: required columns

    def get_pdf_content(self,
                        url: str):
        """
        :param url: target url to get pdf content
        :return: string-like text of content
        """
        r = requests.get(url)
        with open('./cache/' + self.fn, 'wb+') as f:
            f.write(r.content)
        t = ph.extract_text('./cache/' + self.fn)
        return t

    def multi_decoder(self,
                      s: bytes):
        """
        :param s: bytes-format to be decoded with
        :return: decoded string
        """
        try:
            ds = str(s, 'utf_8_sig')
        except UnicodeDecodeError:
            try:
                ds = str(s, 'gbk')
            except UnicodeDecodeError:
                try:
                    ds = str(s, 'GB18030')
                except UnicodeDecodeError:
                    ds = str(s, 'gb2312', 'ignore')
        return ds

    def get_page(self,
                 p: int,
                 shuffle_id: bool):
        """

        :param p: int: page number
        :param shuffle_id: bool: generate random callback file id
        :return: dict containing data from page p
        """
        page_no = str(p)
        begin_page = str(p)
        end_page = str(p) + '1'
        callback_id = str(np.random.randint(90000, 99999)) if shuffle_id else '92456'
        _id = str(1596693256072 + int(p - 1))
        url = '''http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback{}&siteId=28&sqlId=BS_KCB_GGLL&extGGLX=&stockcode=&channelId=10743%2C10744%2C10012&extGGDL=&order=createTime%7Cdesc%2Cstockcode%7Casc&isPagination=true&pageHelp.pageSize=15&pageHelp.pageNo={}&pageHelp.beginPage={}&pageHelp.cacheSize=1&pageHelp.endPage={}&type=&_={}'''
        url = url.format(callback_id, page_no, begin_page, end_page, _id)

        headers = {
            'User-Agent': choice(self.ua_library),
            'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/',
            'Host': 'query.sse.com.cn'}

        rsp = requests.get(url=url, headers=headers)
        rsp_str = self.multi_decoder(rsp.content)

        if len(rsp_str) < 500:
            print('Warning, scrapped file may be incorrect from page {}.'.format(page_no))
        else:
            pass

        rsp_str = rsp_str.replace('jsonpCallback' + callback_id, '')
        rsp_str = rsp_str[1:-1]
        json_str = json.loads(rsp_str)
        d = json_str.get('result')
        d_final = []
        for dd in d:
            dd['unique_id'] = str(np.random.random()).replace('.', '')
            d_final.append(dd)
        return d_final

    def extract_info(self,
                     d: list):
        """

        :param d: a list composed of dictionaries that need to extract information from
        :return: rc, extracted information
        """
        g_info = [[x.get(y) for y in self.rc] for x in d]

        return g_info