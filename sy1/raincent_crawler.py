import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import xlwt
import random

page_start = 1  # 用户输入
page_end = 45  # 用户输入


# def openlink(self, link):
#     maNum = 10
#     for tries in range(maNum):
#         try:
#             req = urllib.request.Request(link, headers=self.headers)
#             response = urllib.request.urlopen(link)
#             return response
#         except:
#             if tries < (maNum - 1):
#                 continue
#             else:
#                 print("Has tried %d times to access url %s, all failed!", maNum, link)
#                 break


def next_page(soup):
    # nextUrls = soup.find_all("div", class_="dw_page")
    # href = nextUrls[0].find("a")
    # url_new = href['href']
    # return str(url_new)
    nextUrls = soup.find("div", class_="text-c")
    # href = nextUrls.find("a")
    # url_new = nextUrls['href']
    result = nextUrls.find_all("a", class_="a1")
    url_new = "http://www.raincent.com/" + result[-1]['href']
    print(url_new)
    return url_new


def _raincent_list_crawler(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    soup = BeautifulSoup(content, "lxml")
    main_part = soup.find("div", class_="main")
    # href = nextUrls.find("a")
    # url_new = nextUrls['href']
    listUrls = main_part.find_all("li", class_="clear")
    links = []
    for child in listUrls:
        # pattern = re.compile("<a href=\"(.*?)\" onmousedown=\"\" target=\"_blank\"", re.S)
        m = child.find("a")
        links.append(m['href'])
        # print(pattern.findall(m))

    return links


def _raincent_info_crawler(links):
    for url in links:
        # url = 'http:' + url
        # test = "jobs.51job.com"
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            res = urllib.request.Request(url, headers={'User-Agent': user_agent})
            response = urllib.request.urlopen(res)
            content = response.read().decode('utf-8')
            soup = BeautifulSoup(content, "lxml")

            main_part = soup.find("div", class_="main w1060")
            title = main_part.find("strong")
            article = main_part.find("div", class_="content")

            # print(url)
            print(tag_deleter(str(title)))  # title
            print(tag_deleter(str(article)))
            global count
            if len(tag_deleter(str(title))) <= 30000 and len(tag_deleter(str(article))) <= 30000:
                table.write(count, 0, tag_deleter(str(title)))
                table.write(count, 1, tag_deleter(str(article)))
                table.write(count, 2, url)
                count = count + 1
                # print(count)
                file.save('result.xls')
            else:
                pass
            # time.sleep(random.uniform(0, 0.4))
        except:
            pass
    #         global count
    #         for _ in list:
    #             print(_)
    #         for i in range(len(list)):
    #             list[i].encode('utf-8')
    #             table.write(count, i, list[i])
    #         count = count + 1
    #         time.sleep(random.uniform(0, 0.8))
    #         file.save('demo.xls')
    #     else:
    #         pass
    #
    return len(links)


def tag_deleter(s):
    # s = re.sub("</?p>", "", s)
    # s = re.sub("<br/>", "", s)
    # s = re.sub("</?b>", "", s)
    # s = re.sub("</?span>", "", s)
    # s = re.sub(" ", "", s)
    s = re.sub("\t", "", s)
    s = re.sub("\n", "", s)
    s = re.sub("\r", "", s)
    s = re.sub("<.*?>", "", s)
    # s = re.sub("\xa0", "", s)
    # s = re.sub("<pre>", "", s)
    # s = re.sub("</?li>", "", s)
    # s = re.sub("</?ol>", "", s)
    # s = re.sub("<pclass=\"MsoNormal\">", "", s)
    # s = re.sub("</?strong>", "", s)
    # s = re.sub("<span class=\"lname\">", "", s)
    # s = re.sub("<pstyle=\"text-indent:2em;\">", "", s)
    # s = re.sub("</?div>", "", s)
    return s


url = "http://www.raincent.com/list-10-" + str(page_start) + ".html"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
req = urllib.request.Request(url, headers={'User-Agent': user_agent})
response = urllib.request.urlopen(req)
content = response.read().decode('utf-8')
soup = BeautifulSoup(content, "lxml")
count = 0
file = xlwt.Workbook()
table = file.add_sheet('表格1', cell_overwrite_ok=True)
# file.save('demo.xls')

for i in range(page_end - page_start):   # 括号内参数设定爬取的总页面数目，此处设定20则爬取共21面信息，约共1000条
    print("正在爬取第" + str(page_start + i) + "面")
    links_list = _raincent_list_crawler(url)
    length = _raincent_info_crawler(links_list)
    url = next_page(soup)
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    soup = BeautifulSoup(content, "lxml")
    print("总计" + str(length) + "条信息")
    # print("正在爬取第" + str(i+2) + "面")
