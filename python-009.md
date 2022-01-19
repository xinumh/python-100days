

```python
import requests
import re
from bs4 import BeautifulSoup
from tqdm import trange

headers = {
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
}



def get_download (url, novel):
  
  r = requests.get(url, headers)
  r.encoding = 'urf8'
  html = r.text

  # 最主要的功能是从网页抓取数据
  data = BeautifulSoup(html, "html.parser")
  r.status_code
  print('请求状态：', r.status_code)

  # 标题
  section_name = data.title.string
  # 内容
  section_text = data.select('#bgdiv .border_l_r #content p')[0].text
  # 内容格式化
  section_text = re.sub( '\s+', '\r\n\t', section_text).strip('\r\n')

  with open(novel, 'a', encoding='utf-8') as f:
    f.write(section_name + "\n")
    f.write(section_text + "\n")

  pt_nexturl = 'var next_page = "(.*?)"'
  nexturl_num = re.compile(pt_nexturl).findall(str(data))
  nexturl_num = nexturl_num[0]
  
  print('nexturl_num', nexturl_num)
  return nexturl_num


if __name__ == '__main__':
  
  url = 'http://www.lewenge.org/books/21/21335/6381842.html'
  novel = '相见欢.txt'
  num = 2289999999
  
  for i in trange(num):
    nexturl = get_download(url, novel)
    print('nexturl', nexturl)
    url = 'http://www.lewenge.org/books/21/21335/'+nexturl
    if(nexturl == 'http://www.lewenge.org/books/21/21335/'):
      break

```