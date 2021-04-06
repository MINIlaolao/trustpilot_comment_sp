def sp(count_page, website):
    count_page_str = "page=" + count_page.__str__() + "&"

    page = r"https://uk.trustpilot.com/review/" + website + "?" + count_page_str + "stars=4&stars=5"

    html = urllib.request.urlopen(page)

    soup = BeautifulSoup(html, "html.parser")
    jsonlist = []
    for items in soup.find_all("script", type="application/json"):
        if items.attrs["data-initial-state"] == "review-info":
            data = json.loads(json.dumps(str(items.contents[0]), ensure_ascii=False))
            jsonlist.append(data)
            print(data)
    time.sleep(random.randint(1, 3))
    return jsonlist



if __name__ == '__main__':
    # base website
    base_website = "www.samsungrecycle.co.uk"

    jsonresult = []
    # start_page_num end_page_num
    for i in range(1, 148):
        jsonresult.append(sp(i, base_website))
    jsons = json.loads(json.dumps(jsonresult))

    print(jsons)
