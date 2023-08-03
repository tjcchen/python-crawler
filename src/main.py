#
# Crawl reviews with Python from TripAdvisor
#
# List: https://www.tripadvisor.com/Restaurants-g155019-Toronto_Ontario.html
# Detail: https://www.tripadvisor.com/Restaurant_Review-g155019-d23978218-Reviews-Casa_Madera-Toronto_Ontario.html
#
# Install packages with pip: python3 -m pip install "requests"
#

import requests    # send requests
import parsel      # analyze response data


def main():
    url = "https://www.tripadvisor.com/Restaurants-g155019-Toronto_Ontario.html"
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
    link_list = selector.css(".Lwqic.Cj.b::attr(href)").getall()

    print(link_list)
    
    # 4. send request to each detail link
    # processing...
    for link in link_list:
        link = "https://www.tripadvisor.com/" + link
        detail_html = requests.get(link, headers=headers).text
        detail_selector = parsel.Selector(detail_html)
        detail_title = detail_selector.css(".HjBfq::text").get()
        print(detail_title)
    

if __name__ == "__main__":
    main()
