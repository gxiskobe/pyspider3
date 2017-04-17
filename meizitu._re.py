from urllib.request import urlopen
from pandas import json
import requests
import os
import re
#h获取链接
def get_one_page(url):
    response = requests.get(url).text
    # print(response.text)
    return response
#获得主页内容的各个子网页链接
def parse_total_page(response):
    pattern = re.compile('<li><a href=(.*?)target=',re.S)
    # pattern = re.compile(r'[a-zA-z]+://[^\s]*', re.S)
    items = re.findall(pattern,response)
    # print(items)
    # for item in items:
    #     print(item)
    #     print(json.loads(item))
    # print(len(items))
    return items

#获取所有网页图片名称
def get_image_name(response1):
    result = get_one_page(json.loads(response1))
    pattern = re.compile('<h2 class="main-title">(.*?)</h2>',re.S)
    items = re.search(pattern,result)
    print(u'图片名称为：',items.group(1))
    return items.group(1)

#获取每个网页包含的图片数量
def get_image_number(response1):
    result = get_one_page(json.loads(response1))
    pattern = re.compile('<span>(.*?)</span>', re.S)
    items = re.findall(pattern, result)
    print(u'此图片数量为：',items[8])
    return items[8]

#获取每个网页的图片地址
def get_image_url(response1,number):
    for i in range(1, 10):
        print(i)
        new_response = json.loads(response1) + '/' + str(i)
        print(new_response)
        result = get_one_page(new_response)
        pattern = re.compile('<img src="(.*?)" alt', re.S)
        items = re.search(pattern, result)
        print(u'获取到地址为：', items.group(1), u'的图片')
        return items.group(1)

#保存图片
def save_image(detailUrl,path,name):
    # picture = urlopen(detailUrl)
    img = requests.get(detailUrl)
    print(u'正在保存链接为：',detailUrl,'的图片')
    string =  'D:\picture\%s\%s' % (path,name)
    E = os.path.exists(string)
    if not E:
        f = open(string, 'wb')
        f.write(img.content)
        f.close()
    else:
        print(u'图片已经存在，跳过')
        return False

def make_dir(path):
    path = path.strip()
    E = os.path.exists(os.path.join('D:\picture',path))
    if not E:
        # 创建新目录,若想将内容保存至别的路径（非系统默认），需要更环境变量
        # 更改环境变量用os.chdir()
        os.makedirs(os.path.join('D:\picture', path))
        os.chdir(os.path.join('D:\picture', path))
        print(u'成功创建名为', path, u'的文件夹')
        return path
    else:
        print(u'名为', path, u'的文件夹已经存在...')
        return False
def main():
    url = "http://www.mzitu.com/"
    response = get_one_page(url)
    items = parse_total_page(response)
    for item in items:
        # 获取所有网页图片名称
        path = get_image_name(item)
        # 获取每个网页包含的图片数量
        number = get_image_number(item)
        # 获取每个网页的图片地址
        make_dir(path)
        for i in range(1, int(number)+1):
            new_response = json.loads(item) + '/' + str(i)
            result = get_one_page(new_response)
            pattern = re.compile('<img src="(.*?)" alt', re.S)
            items = re.search(pattern, result)
            print(u'获取到地址为：', items.group(1), u'的图片')
            name = 'picture'+str(i)+'.jpg'
            save_image(items.group(1),path,name)
if __name__ == '__main__':
    main()
