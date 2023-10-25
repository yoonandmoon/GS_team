import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_news(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    # 기본값 설정
    title = "???"
    date = "???"
    media = "???"
    content = "???"

    # 제목 가져오기
    title_element = soup.select_one("h2#title_area span")
    if title_element:
        title = title_element.text

    # 날짜 가져오기
    date_element = soup.select_one("span.media_end_head_info_datestamp_time")
    if date_element and 'data-date-time' in date_element.attrs:
        date = date_element['data-date-time']

    # 매체명 가져오기
    media_element = soup.select_one("a.media_end_head_top_logo img")
    if media_element and 'title' in media_element.attrs:
        media = media_element['title']

    # 기사 내용 가져오기
    content_element = soup.select_one("div#newsct_article")
    if content_element:
        content = content_element.text.replace("\n", "")

    return (title, date, media, content, URL)

def get_news_list(keyword, startdate,enddate):
      li = []
      h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'Referer': 'https://search.naver.com/search.naver?where=news&query=%ED%85%8C%EC%8A%AC%EB%9D%BC&sm=tab_opt&sort=2&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0', 'cookie': '...'}
      count = 0
      for d in pd.date_range(startdate, enddate):
          str_d = d.strftime("%Y.%m.%d")
          page = 1
          print(str_d)
          while True:
              print(page)
              start = (page - 1) * 10 + 1
              URL = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=2&photo=0&field=0&pd=3&ds={1}&de={2}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{3}to{4},a:all&start={5}".format(keyword, str_d, str_d, str_d.replace(".", ""), str_d.replace(".", ""), start)

              res = requests.get(URL, headers=h)
              soup = BeautifulSoup(res.text, "html.parser")

              if soup.select_one(".api_noresult_wrap"):
                  break

              news_list = soup.select("ul.list_news li")

              for item in news_list:
                  if len(item.select("div.info_group a")) == 2:
                      li.append(get_news(item.select("div.info_group a")[1]['href']))
                      print(li[count][1])
                      count = count + 1
              page = page + 1

      # DataFrame을 생성합니다
      df = pd.DataFrame(li, columns=['title', 'date', 'media', 'content', 'url'])

      # DataFrame을 CSV 파일로 저장합니다
      df.to_csv('news_data08.csv', index=False)  # 이 코드는 DataFrame을 'news_data.csv'라는 이름의 CSV 파일로 저장합니다

      print(count)

get_news_list('GS건설','2023.08.01','2023.09.02')