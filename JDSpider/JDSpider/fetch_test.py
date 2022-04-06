import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


if __name__ == '__main__':
    opt = Options()
    opt.add_argument('-headless')
    driver = webdriver.Chrome(chrome_options=opt)
    driver.get('https://item.jd.com/10044196485220.html')
    print(driver.page_source)
