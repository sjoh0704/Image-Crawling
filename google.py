from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
from concurrent import futures

def make_folder(directory):
    print("images/{0} 디렉토리 생성".format(directory))
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def image_crawling(word):
    make_folder("images/"+word)
    path='/home/seung/projects/image/chromedriver' 
    driver = webdriver.Chrome(path)
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(word)
    elem.send_keys(Keys.RETURN)
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    for i, image in enumerate(images):
        try:
            image.click()
            time.sleep(0.5)
            imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imgUrl, "images/{0}/{1}.jpg".format(word, i+1))
            print("{0} image{1} 생성".format(word, i+1))
        except Exception as e:
            print(e)
            

    driver.close()
    return "---------{} download done---------".format(word)

if __name__ == "__main__":
    make_folder("images")

    search = ["고양이", "강아지"]
    with futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(image_crawling, s) for s in search]
 
    for f in futures.as_completed(results):
        print(f.result())