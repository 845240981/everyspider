import requests
from requests.exceptions  import  RequestException
import re
import json
from multiprocessing import Pool


def get_text(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items: 
        yield { 'rank' : item[0],
                'piture':item[1],
                'moviename':item[2],
                'moviestar':item[3].strip()[3:],
                'time':item[4][5:],
                'score':item[5]+item[6] }
def wirte_file(content):
    with open ('1.txt' , 'a',encoding='utf-8') as f :
        f.write(json.dumps(content,ensure_ascii=False )+'\n')
# dumps是将dict转化成str格式，loads是将str转化成dict格式。
# json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False：
#'a'：以追加模式打开。若文件存在，则会追加到文件的末尾；若文件不存在，则新建文件。


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_text(url)
    items = parse_one_page(html)
    for item in items:
        print(item)
        wirte_file(item)


if __name__=='__main__':
    pool = Pool()
    pool.map(main , [i*10 for i in range(10)])
    pool.close()
    pool.join()
