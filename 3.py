import requests
from requests.exceptions import  RequestException
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool

def get_html(url):
    try:
        respond = requests.get(url)
        if respond.status_code == 200:
            respond.encoding = respond.apparent_encoding

            return respond.text
        return None
    except RequestException:
        return None

def jiexi(html):
    soup=BeautifulSoup(html , 'html.parser')


    #pattern= re.compile('<table width="100%">.*?<img src="(.*?)".*?title="(.*?)"'
                        #+'.*?<p class="pl">(.*?)</p>.*?rating_nums">(\d+)</span>.*?inq">(.*q)</span>',re.S)

    #items=re.findall(pattern,html)
    #print(items)

    #saying_soup = soup.findAll('span',{'class':'inq'})
    #sayingslist= [saying.string for saying in saying_soup]

    image_soup= soup.findAll('img',{'width':"64"})
    image_list=[image.attrs['src'] for image in image_soup]

    movie_soup = soup.find_all('div',{'class':'pl2'})
    name_list=[i.find('a').attrs['title'] for i in movie_soup]

    score_soup = soup.findAll('span', {'class': 'rating_nums'})
    scorelist= [score.string for score in score_soup]

    for i  in range(len(scorelist)):
        yield {
            'book_name':name_list[i],
            'book_image':image_list[i],
            'book_score':scorelist[i],
            #'book_comment':sayingslist[i]
        }



def write_file(content):
    with open('4.txt','a',encoding='utf-8') as f :
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def main(start):
    url = 'https://book.douban.com/top250?start='+str(start)
    html = get_html(url)
    for project in jiexi(html):
        write_file(project)
        print(project)

if __name__ == '__main__':
    pool=Pool()
    numbner=pool.map(main,[i*25 for i in range(10)])

    pool.close()
    pool.join()