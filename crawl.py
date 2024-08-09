import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm
import csv
from urllib.parse import quote
import html

# headers = {
#   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
#   'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#   'Content-Type': "application/x-www-form-urlencoded",
#   'accept-language': "zh,zh-CN;q=0.9",
#   'cache-control': "max-age=0",
#   'origin': "https://www.ncbi.nlm.nih.gov",
#   'priority': "u=0, i",
#   'referer': "https://www.ncbi.nlm.nih.gov/pmc/?term=\"Reviews+in+Urology\"%5BJournal%5D+AND+(\"2019%2F01%2F01\"%5BPDat%5D+%3A+\"2019%2F12%2F31\"%5BPDat%5D)",
#   'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
#   'sec-ch-ua-mobile': "?0",
#   'sec-ch-ua-platform': "\"Windows\"",
#   'sec-fetch-dest': "document",
#   'sec-fetch-mode': "navigate",
#   'sec-fetch-site': "same-origin",
#   'sec-fetch-user': "?1",
#   'upgrade-insecure-requests': "1",
#   'Cookie': "ncbi_sid=CE8A5D9D69A0BF41_0993SID; WebEnv=1fkQz_lawnnV9jcCohC_4BU6-z_JjGJZ73kG00feeXUkB%40CE8A5D9D69A0BF41_0993SID; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAcAQrgIwCshAbAJzW7UDMAgiQAzscf4kBirNhAHQBbOCUogANCADGAG2QyA1gDsoADwAumUK0wgAzgFcARsKgqjkgGbI5USZoCGJgAoB7MGCgRJBi6hwmu4ABEbIALSIUHLeEBHQ/pphkSoyJshgnnERAO4QTl4+KRFpGVlF8SZOBoqSiUZymgZwSZrIKgDmBpIy7iqaFpq97nJ+sBZwfXJSICT6xmYWRnA8dg7+KoHBcOaWksJOHX0DQ7MM1Pr4lNd60gAselj4+GQA7Ayz9/f68oqqGm0DzI+nmDwkWGsTjk/i+b309xuX3wCPw8IelywJiMmmCKjghTAcgAnjZ1pIyplsj4IvJ3P4Itjcf1ZmQniBWfMsKyAEz6bDQJyDEJrewgAC+0iMKjk7icqDUWh0IAYnywmggRig5x+6s12ukDBR3MNmJA1zRfIe7JeZFeX11IGlsvliqBIHuIKwVpAZAhvoYIOk730dxAlC5IDe+E+ktk7mEwn6buVfKwQ2gAC9zvowMIZF99Kh3DJjMJWfpZv7i6WjOXpPCsIhNMIZtJjSAeWGzagoFDGu6SJGwXM1SqftISI7/E4IDJELNxPpoW25o2QFCYQa5h3N7DpF3+QRiOQqLR6Mw2JxONw+AIRGIJAfIxmoJmMHmZBga2WMAA5AB5P9cFmHk0xAXJIMESloLkYRoOQRBBE6dwYFAs0SGoQ9DXZNh8DDBhhywgjwLYR4vjHVhBEeQQwzIMdKAYH0yEdRh5nFcUgA==="
# }

onlyheaders = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
  'Cookie': "ncbi_sid=CE8C3F7369521111_0435SID; pmc-frontend-csrftoken=RyaSoiwaxTjcquJ6vDxbgjnytMRJHAA4; _gid=GA1.2.1201218639.1723188384; _gat_dap=1; _ce.irv=returning; cebs=1; _ce.clock_event=1; _ce.clock_data=57,46.232.121.223,1,d88a03f1175846c9a610db9271f1b11b,Chrome,HK; cebsp_=1; WebEnv=1n1ImkqZofD1IYkYSm9tLiKxr6It9kVKArw37oZu-w-5R@CE8C3F7369521111_0435SID; _ce.s=v~945ef309ef98e131259bc258ca3b2185159dd729~lcw~1723188402316~lva~1723188384779~vpv~1~v11slnt~1721049513842~v11.cs~156325~v11.s~af46f520-5620-11ef-a7c5-2767ee9602f8~v11.sla~1723188402418~v11.send~1723188399904~lcw~1723188402419; _ga_DP2X732JSX=GS1.1.1723188384.12.1.1723188405.0.0.0; _ga=GA1.1.797156739.1721049365; _ga_CSLL4ZEK4L=GS1.1.1723188384.12.1.1723188405.0.0.0; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAcAggCwCMuAbBQEICsAnAOwBi+pADJ114wMz3sKDAHQBbOKUYgANCACuAOwA2AewCGqBVAAeAF0ygATJhBQFu6AC8ZIXibCiAxjeInUKxwGc5om7RM2FG4e3r6yUliIuqJKNvgmhuw29G5QAGZqckr6sqSkJvm5dliGTEKG8bmuWJ5QahCOiDakQVhqSrG5ESAZSrXN8Vi9/bKJJnhEZJQ0DCxs3At8AkL0YhJSo/lYZhZQlhgOjhjuXj4YAHIA8ue4NobGWADuz8IKjgBGyK9Koq/IiMIAOYqGB3FJYUi0XhBWS8JJYfAUVywrYgSHQmy8B4gfCGZG2YogCxyKCY6pEiAkzGDECY8Fo2gVFzwkAUXikfHEQnsYTEHlJWTEcmKVQaLR6Fz+LACkBQkx8uyyWjkxj3PytVm8fG0boyiio0j4fggAC+JqAA=="
}


def process(dirname,search_term,year):
    main_url = "https://www.ncbi.nlm.nih.gov/pmc"

    search_term_in_url=quote(search_term)

    search_url = f'https://www.ncbi.nlm.nih.gov/pmc/?term={search_term_in_url}'

    filename = dirname + "[journal]" + year

    try:
        search_response=requests.get(search_url,headers=onlyheaders)
    except Exception as e:
        # 查询失败
        with open('error_search_response.txt', 'a+', encoding='utf-8') as ef:
            ef.write('{}\n'.format(filename, e))
    soup = BeautifulSoup(search_response.text, 'html.parser')
    form = soup.find('form', {'name': 'EntrezForm'})
    if form:
        data = {}
        for input_field in form.find_all('input'):
            data[input_field.get('name')] = input_field.get('value')
        count=data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_ResultsSearchController.ResultCount']
        if count=='0':
            with open('no_item.csv', 'a+', encoding='utf-8', newline='') as noitemf:
                noitemdata = []
                noitemdata.append(filename)
                noitemdata.append(search_url)
                csv.writer(noitemf).writerow(noitemdata)
            return
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPresentation'] = "DocSum"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPageSize'] = "20"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sSort'] = "none"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.SendTo'] = "File"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FFormat'] = "XML"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FSort'] = ""
        data['email_format'] = "DocSum"
        data['email_sort'] = ""
        data['email_count'] = "20"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FileFormat'] = "XML"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPresentation2'] = "DocSum"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPageSize2'] = "20"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sSort2'] = "none"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FFormat2'] = "DocSum"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FSort2'] = ""
        data['email_format2'] = "DocSum"
        data['email_sort2'] = ""
        data['email_count2'] = "20"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_MultiItemSupl.Pmc_RelatedDataLinks.rdDatabase'] = "rddbto"
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Discovery_SearchDetails.SearchDetailsTerm'] = search_term_in_url
        data['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.HistoryDisplay.Cmd'] = "file"
        data['EntrezSystem2.PEntrez.DbConnector.Cmd'] = "file"
        data['p$a'] = "EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.SendToSubmit"
        data['p$l'] = "EntrezSystem2"
        try:
            location_response = requests.post(main_url, data=data, headers=onlyheaders, allow_redirects=False)
            headers = location_response.headers
        except Exception as e:
            # 查找location失败
            with open('error_location_response.txt', 'a+', encoding='utf-8') as ef:
                ef.write('{}\n'.format(filename, e))
        # 查找location失败
        if location_response.status_code!=301:
            with open('error_location_response.txt', 'a+', encoding='utf-8') as ef:
                ef.write('{}\n'.format(filename, e))

        download_url = "https://www.ncbi.nlm.nih.gov" + headers['Location']
        try:
            download_xml(dirname,download_url, filename)
        except Exception as e:
            # 下载xml失败
            with open('error_xml_response.txt', 'a+', encoding='utf-8') as ef:
                ef.write('{}\n'.format(filename, e))

def create_fold(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_xml(dirname,download_url,filename):
    with open('download_url.csv', 'a+', encoding='utf-8',newline='') as urlf:
        urldata=[]
        urldata.append(filename)
        urldata.append(download_url)
        csv.writer(urlf).writerow(urldata)

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        # 将文件内容写入本地文件
        with open(f"./results/{dirname}/{filename}.xml", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    create_fold("results")

    # 读取 Excel 文件
    df = pd.read_excel('待处理.xlsx')  # 将 'your_file.xlsx' 替换为您的 Excel 文件的实际路径和文件名

    dirname = ""
    # 遍历行
    for index, row in tqdm(df.iterrows()):
        # 遍历列
        for column in tqdm(df.columns):
            if column == "name":
                dirname = row[column].replace(":","-").replace("/","-").replace("\\","-").replace("*","-").replace("?","-").replace("\"","-").replace("<","-").replace(">","-").replace("|","-")
                dirname = html.unescape(dirname)
                if len(dirname)>50:
                    dirname = dirname[:50]
                    dirname = dirname.rstrip()
                create_fold(f"./results/{dirname}")
            else:
                year=str(column)
                search_term = row[column]
                search_term = html.unescape(search_term)
                process(dirname,search_term,year)



if __name__ =="__main__":
    main()