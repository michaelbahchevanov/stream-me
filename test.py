# Web scraping is bad and this is totally depricated!
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup as bs
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.options import Options

# def setup_selenium():
#     driver_options = Options()
#     driver_options.add_argument('--headless')
#     path_to_driver = '/usr/bin/chromedriver'
#     driver = webdriver.Chrome(path_to_driver, options=driver_options)
#     return driver

# def interceptor(request):
#     del request.headers['User-Agent']
#     request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

# def test(driver=None, url=''):
#     driver.get(url)
#     html = driver.execute_script('return document.body.innerHTML;')
#     soup = bs(html, 'html.parser')

#     print([row.text for row in soup.find('table').thead.tr.find_all('th')[2:11]])

# def main():
#     driver = setup_selenium()
#     driver.request_interceptor = interceptor
#     test(driver=driver, url=url)

# if __name__=='__main__':
#    main()