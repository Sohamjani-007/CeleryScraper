import time
from selenium import webdriver
import requests

from scraper.models import Proxy


def scrape_and_save_proxy_data():
    url = 'https://geonode.com/free-proxy-list'
    # Set up the Chrome webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # To run Chrome in headless mode (without opening a browser window)
    driver = webdriver.Chrome(options=options)

    # Open the website
    driver.get(url)  # URL of the public website you want to analyze

    # Let the website load for 6 seconds
    time.sleep(6)

    # Get all the network calls
    network_calls = driver.execute_script("return window.performance.getEntries();")

    # looping through all the calls to fetch the list API from it.
    for call in network_calls:

        # name is hardcoded as we found it from the network call
        proxy_list_organdasn = "https://proxylist.geonode.com/api/organdasn?limit=100&page=1"
        if call.get("name") == proxy_list_organdasn:
            proxylist_geonode_api = proxy_list_organdasn[:proxy_list_organdasn.find('?')]
            return proxylist_geonode_api


def getting_web_scarped_proxy_data():
    """
    Function to get the proxies from geonode and save them in the model : Proxy.
    :return:
    """
    # now we will provide additional headers. As requests passed in the
    # "https://proxylist.geonode.com/api/organdasn?limit=100&page=1" is authenticated. which results in 403.

    headers = {
        'authority': 'proxylist.geonode.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'if-none-match': 'W/"ad8a-1pm1LBuj4AcnksNSeSspBg1i6k0"',
        'origin': 'https://geonode.com',
        'referer': 'https://geonode.com/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    for i in range(1, 100):
        params = {
            'limit': '100',
            'page': i,
        }
        response = requests.get(scrape_and_save_proxy_data(), params=params, headers=headers)
        # looping through the found data and extracting all the elements.
        for network_data in response.json().get("data"):
            # Saving all the data in the model :
            proxy = Proxy.objects.create(ip=network_data.get("ip"), port=network_data.get("port"), protocol=network_data.get("protocols"), country=network_data.get("country"), uptime=network_data.get("upTime"))
            proxy.save()
            print(proxy)