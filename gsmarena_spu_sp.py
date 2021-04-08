# encoding:utf-8
import http.client
from bs4 import BeautifulSoup
import json


def search_url(key):
    conn = http.client.HTTPSConnection("www.gsmarena.com")
    payload = ''
    conn.request("GET", 'https://www.gsmarena.com/res.php3?sSearch=' + key, payload)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    soup = BeautifulSoup(data, 'lxml')
    div = soup.find(name="div", attrs={"class": "makers"})
    a_href_list = div.find_all(name="a")
    attributes = []
    conn.close()
    for href in a_href_list:
        attributes.append(choose_page(href.get('href'), key))
    return attributes


def choose_page(url, brand):
    global models, colors
    conn = http.client.HTTPSConnection("www.gsmarena.com")
    payload = ''
    conn.request("GET", "/" + url, payload)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    soup = BeautifulSoup(data, "lxml")
    name = str(soup.find(name="title").contents[0])
    name = name[len(brand) + 1:name.find(" -")]
    try:
        colors = str(soup.find(name="td", attrs={"data-spec": "colors"}).contents[0]
                     if soup.find(name="td", attrs={
            "data-spec": "colors"}) else None)

        models = str(soup.find(name="td", attrs={"data-spec": "models"}).contents[0]
                     if soup.find(name="td", attrs={
            "data-spec": "models"}) else None)

        colors = colors.split(", ") if colors is not None else []
        models = models.split(", ") if models is not None else []
    except AttributeError:
        print("AttributeError:" + name)
    finally:
        conn.close()
    capacities = soup.find(name="td", attrs={"data-spec": "internalmemory"}).contents
    new_capacities = []
    for capacity in capacities:
        capacity = str(capacity).split(",")
        for x in capacity:
            new_capacities.append(int(x[:x.find("GB")].strip()))
    # 自定义属性
    attribute = {'name': name,
                 'spec':
                     {'color': colors, 'model': models, "capacity": list(set(new_capacities)),
                      'carrier': ["Verizon", "Sprint", "AT&T", "T-Mobile", "Generic", "Unknown",
                                  "Locked"]},
                 'category': '手机',
                 'brand': brand,
                 'disable': 0,
                 }
    return attribute


def output(arry, key):
    load_dict = json.dumps(arry, ensure_ascii=False)
    file_path = key + '.json'
    f2 = open(file_path, 'w', encoding="utf-8")
    f2.write(load_dict)
    f2.close()
    return file_path


if __name__ == '__main__':
    key = input("输入品牌号：")
    print("品牌:" + key)
    attribute = search_url(key)
    print('file_path:' + output(attribute, key))

    # choose_page("/huawei_p30_pro-9635.php")
