import csv
import requests
from lxml import etree
import re
import time

KEYWORD = '书法征稿启事'

def timeformat(stamp):
  second_stamp = time.localtime(stamp)
  formatTime = time.strftime("%Y-%m-%d %H:%M", second_stamp)
  return formatTime

def get_page_text(number):
  HOST = 'http://weixin.sogou.com/'
  entry = HOST + "weixin?type=2&query="+KEYWORD+"&page="+str(number)
  headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
  res  = requests.get(entry.format(number), headers) # 第一页
  res.encoding = 'utf-8'
  return res.text

def parse_page(text):
  html = etree.HTML(text)
  
  """ 文章标题 """
  title_list = list()
  title_element_list = html.xpath("//div[@class='txt-box']/h3/a")
  for title_element in title_element_list:
    title = title_element.xpath("string(.)")
    title_list.append(title)
  print(title_list)
  
  """ 文章链接 """
  link_list = list()
  base_url = "http://weixin.sogou.com"
  links = html.xpath("//div[@class='txt-box']/h3/a/@href")
  for link in links:
    print(link)
    href = "".join(list(base_url)+list(link))
    link_list.append(href)
  print(link_list)
  
  """ 发布时间 """
  publish_time_list = list()
  time_list = list()
  time_element_list = html.xpath("//div[2]/div/span")
  for time_element in time_element_list:
    time = time_element.xpath("string(.)")
    time_list.append(time)
  for t in time_list:
    t_str = re.findall(r"\d+\.?\d", t)
    last = ''.join(t_str)
    publish_time_list.append(timeformat(int(last)))
    
    
  print(publish_time_list)
  
  
  
  return zip(title_list, link_list, publish_time_list)

def save_to_csv(result, filename):
  with open(filename, 'a', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(result)



def main():
  for number in range(1, 3):
    text = get_page_text(number)
    result_list = parse_page(text)
    for res in result_list:
      save_to_csv(res, filename=KEYWORD +'_msg.csv')

  
  
if __name__ == '__main__':
  main()