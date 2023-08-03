#
# Crawl data with Python from TripAdvisor
#
# List: https://www.tripadvisor.com/Restaurants-g155019-Toronto_Ontario.html
# Detail: https://www.tripadvisor.com/Restaurant_Review-g155019-d23978218-Reviews-Casa_Madera-Toronto_Ontario.html
#
# Install packages with pip: python3 -m pip install "requests"
#

import requests            # send requests
import parsel              # analyze response data
import re                  # regular expression
import csv                 # store data in csv format
import concurrent.futures  # multi-threads
from datetime import datetime


def main():
    # csv header
    with open("tripadvisor.csv", mode="a", newline="", encoding="utf-8") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["store_name", "comment_count", "address", "phone", "website", "link"])

    url = "https://www.tripadvisor.com/Restaurants-g155019-Toronto_Ontario.html?t=" + str(datetime.now().timestamp())
    headers = {
        "Content-Type": "text/html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # 1. send http request
    response = requests.get(url, headers=headers)
    # 2. fetch data (html source code)
    html_data = response.text
    # 3. dissect the data
    selector = parsel.Selector(html_data)
    # 3.1 retrieve all the a tag href attributes value
    link_list = selector.css(".RfBGI a::attr(href)").getall()
    
    print(link_list)
    
    # 4. send request to each detail link
    for link in link_list:
        link = "https://www.tripadvisor.com/" + link
        detail_html = requests.get(link, headers=headers).text
        detail_selector = parsel.Selector(detail_html)
        
        # 5. analyze data
        store_name = detail_selector.css(".HjBfq::text").get()
        comment_count = detail_selector.css(".vQlTa.H3:nth-child(2) .AfQtZ::text").get()
        address = detail_selector.css(".vQlTa.H3:nth-child(3) .DsyBj.cNFrA:nth-child(1) .AYHFM::text").get()
        phone = detail_selector.css(".vQlTa.H3:nth-child(3) .DsyBj.cNFrA:nth-child(2) a::text").get()
        website = re.findall("\"website\":\"(.*?)\"", detail_html)[0]
        
        print(store_name, comment_count, address, phone, website, link)
        
        # 6. save data to csv
        with open("tripadvisor.csv", mode="a", newline="", encoding="utf-8") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([store_name, comment_count, address, phone, website, link])


# multi-threads
# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
#         exe.submit(main)


# regular
if __name__ == "__main__":
    main()

