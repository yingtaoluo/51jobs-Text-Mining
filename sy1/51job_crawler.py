import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt
import random
import time
import os

# start = time.time()



def anti_gbk_encoding():
    pass


def next_page(soup):
    nextUrls = soup.find_all("div", class_="dw_page")
    href = nextUrls[0].find_all("a")
    url_new = href[-1]['href']
    return str(url_new)


def _51job_list_crawler(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    content = response.read().decode('gbk')
    soup = BeautifulSoup(content, "lxml")
    listUrls = soup.find_all("p", class_="t1 ")
    links = []
    for child in listUrls:
        # pattern = re.compile("<a href=\"(.*?)\" onmousedown=\"\" target=\"_blank\"", re.S)
        m = child.find("a")
        links.append(m['href'])
        # print(pattern.findall(m))

    return links


def tag_deleter(s):
    # s = re.sub("</?p>", "", s)
    # s = re.sub("<br/>", "", s)
    # s = re.sub("</?b>", "", s)
    # s = re.sub("</?span>", "", s)
    s = re.sub(" ", "", s)
    s = re.sub("\t", "", s)
    s = re.sub("\n", "", s)
    s = re.sub("\r", "", s)
    s = re.sub("<.*?>", "", s)
    s = re.sub("\xa0", "", s)
    # s = re.sub("<pre>", "", s)
    # s = re.sub("</?li>", "", s)
    # s = re.sub("</?ol>", "", s)
    # s = re.sub("<pclass=\"MsoNormal\">", "", s)
    # s = re.sub("</?strong>", "", s)
    # s = re.sub("<span class=\"lname\">", "", s)
    # s = re.sub("<pstyle=\"text-indent:2em;\">", "", s)
    # s = re.sub("</?div>", "", s)
    return s


def company_crawler(soup):
    company = soup.find_all("p", class_="cname")
    try:
        company = company[0].find("a")
        company = company['title']
        return company
    except:
        return ""


def title_crawler(soup):
    title = soup.find_all("div", class_="cn")
    try:
        title = title[0].find("h1")
        title = title['title']
        return title
    except:
        return "\n"


def salary_crawler(soup):
    salary = soup.find_all("div", class_="cn")
    try:
        salary = salary[0].find("strong")
        salary = salary.get_text()
        # salary = tag_deleter(salary)
        return salary
    except:
        return ""


def location_crawler(soup):
    location = soup.find_all("span", class_="lname")
    try:
        location = location[0].get_text()
        return location
    except:
        return ""
    # location = tag_deleter(location)


def company_attrs_crawler(soup):
    attrs = soup.find_all("p", class_="msg ltype")
    result = []
    try:
        attrs = attrs[0].get_text()
        attrs = attrs.split("|")
        for a in attrs:
            result.append(tag_deleter(a))
        # location = tag_deleter(location)
        return result
    except:
        return result


def welfare_crawler(soup):
    default = "\n"
    welfare = soup.find_all("p", class_="t2")
    try:
        welfare = welfare[0].find_all("span")
        # welfare = tag_deleter(welfare[0])
        result = ""
        for w in welfare:
            result = result + w.get_text() + ","
        return result
    except:
        return default


def _51job_info_crawler(links):
    for url in links:
        global repo
        repo.append(url)
        result.write(url + '\n')
        # print(url)

    return len(links)

# # repo.append(url)
#         # url = 'http:' + url
#         test = "jobs.51job.com"
#         # if 0 == 1:  # test in url and url not in repo:
#         #     pass
#             # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#             # res = urllib.request.Request(url, headers={'User-Agent': user_agent})
#             # response = urllib.request.urlopen(res)
#             # content = response.read().decode('gbk')
#             # soup = BeautifulSoup(content, "lxml")
#             # Info = soup.find_all("div", class_="bmsg job_msg inbox")
#             # listTitle = title_crawler(soup)
#             # Company = company_crawler(soup)
#             # Salary = salary_crawler(soup)
#             # Location = location_crawler(soup)
#             # Welfare = welfare_crawler(soup)
#             # company_attrs = company_attrs_crawler(soup)
#             # # listTime =
#             # # pattern = re.compile('<div class=\"bmsg job_msg inbox\">(.*?)<div class=\"mt10\">')
#             # m = re.findall(r'<div class=\"bmsg job_msg inbox\">(.*?)<div class=\"mt10\">', str(Info[0]), re.S)
#             # m[0] = tag_deleter(m[0])
#             # list = []
#             # list.append(listTitle)
#             # list.append(Company)
#             # list.append(Salary)
#             # list.append(Location)
#             # list.append(m[0])
#             # list.append(url)
#             # list.append(Welfare)
#             # try:
#             #     list.append(company_attrs[0])
#             #     list.append(company_attrs[1])
#             #     list.append(company_attrs[2])
#             # except:
#             #     pass
#             # global count
#             # for _ in list:
#             #     print(_)
#             # for i in range(len(list)):
#             #     list[i].encode('utf-8')
#             #     table.write(count, i, list[i])
#             # count = count + 1
#             # time.sleep(random.uniform(0, 1))
#             # file.save('demo.xls')


page_start = 1  # 用户输入
page_end = 23  # 用户输入

url = "http://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2," + str(page_start) + ".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
req = urllib.request.Request(url, headers={'User-Agent': user_agent})
response = urllib.request.urlopen(req)
content = response.read().decode('gbk')
soup = BeautifulSoup(content, "lxml")
count = 0
file = xlwt.Workbook()
table = file.add_sheet('表格1', cell_overwrite_ok=True)
repo = []
length_sum = 0
if os.path.exists('./51job_links.txt'):
    reader = open('51job_links.txt', 'r')
    for line in reader.readlines():
        repo.append(line.strip('\n'))
else:
    result = open('51job_links.txt', 'w')
    # file.save('demo.xls')

    for i in range(page_end - page_start):
        print("正在爬取第" + str(page_start+i) + "面")
        try:
            links_list = _51job_list_crawler(url)
            length = _51job_info_crawler(links_list)
            length_sum = length + length_sum
            url = next_page(soup)
            req = urllib.request.Request(url, headers={'User-Agent': user_agent})
            response = urllib.request.urlopen(req)
            content = response.read().decode('gbk')
            soup = BeautifulSoup(content, "lxml")
            print("总计" + str(length_sum) + "条信息")
        except:
            pass
        # print("正在爬取第" + str(i+2) + "面")

for _ in repo:
    # print(_)
    test = "jobs.51job.com"
    if test in _:
        print(_)
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            res = urllib.request.Request(_, headers={'User-Agent': user_agent})
            response = urllib.request.urlopen(res)
            content = response.read().decode('gbk')
            soup = BeautifulSoup(content, "lxml")
            Info = soup.find_all("div", class_="bmsg job_msg inbox")
            listTitle = title_crawler(soup)
            Company = company_crawler(soup)
            Salary = salary_crawler(soup)
            Location = location_crawler(soup)
            Welfare = welfare_crawler(soup)
            company_attrs = company_attrs_crawler(soup)
            # listTime =
            # pattern = re.compile('<div class=\"bmsg job_msg inbox\">(.*?)<div class=\"mt10\">')
            m = re.findall(r'<div class=\"bmsg job_msg inbox\">(.*?)<div class=\"mt10\">', str(Info[0]), re.S)
            m[0] = tag_deleter(m[0])
            list = []
            list.append(listTitle)
            list.append(Company)
            list.append(Salary)
            list.append(Location)
            list.append(m[0])
            list.append(_)
            list.append(Welfare)
            try:
                list.append(company_attrs[0])
                list.append(company_attrs[1])
                list.append(company_attrs[2])
            except:
                pass
            for _ in list:
                print(_)
            for i in range(len(list)):
                list[i].encode('utf-8')
                table.write(count, i, list[i])
            count = count + 1
            # time.sleep(random.uniform(0, 0.4))
            file.save('demo.xls')
        except:
            pass
    else:
        pass

# end = time.time()
#
# print(end-start)
