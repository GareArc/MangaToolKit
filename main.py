from ast import Break
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from enum import Enum

from pathlib import Path


class Status(Enum):
    END_OF_CH = 1
    END_OF_COMIC = 2
    NEXT_PAGE = 3
    
def make_comic_dir(name: str, ch: int):
    Path(f"./imgs/{name}/ch{ch}").mkdir(parents=True, exist_ok=True)
    

def click_next_page(driver: webdriver.Chrome) -> Status:
    next_page_btn = driver.find_element(by=By.XPATH, value="//a[@id='next']")
    next_page_btn.click()
    
    end_of_ch = True
    end_of_comic = True
    
    # check if it is end of chapter
    try:
        end_of_ch_ele = driver.find_element(by=By.XPATH, value="//*[contains(text(), '本章节已阅览完毕，是否进入下一章节')]")
        print("END OF CHAPTER")
    except Exception:
        end_of_ch = False
        end_of_comic = False
        
    if end_of_ch:
        # click to next chapter
        curr_url = driver.current_url
        while curr_url == driver.current_url:
            try:
                next_ch_btn = driver.find_element(by=By.XPATH, value="//a[contains(text(), '直接进入下一章节')]")
                next_ch_btn.click()
                
                # check if it is end of comic
                try:
                    end_of_comic_ele = driver.find_element(by=By.XPATH, value="//*[contains(text(), '漫画已完结')]")
                    print("END OF COMIC", end_of_comic_ele.text)
                    break
                except Exception:
                    end_of_comic = False
            except Exception:
                pass
            
    if end_of_comic:
        return Status.END_OF_COMIC
    elif not end_of_comic and end_of_ch:
        return Status.END_OF_CH
        
    return Status.NEXT_PAGE


def main():
    name="亲爱的我饱含杀意"
    url = "https://www.manhuagui.com/comic/28765/380637.html"
    driver = webdriver.Chrome()
    driver.get(url)

    end = False
    ch = 1
    pg = 1
    make_comic_dir(name, ch)
    while not end:
        html = driver.page_source
        curr_url = driver.current_url
        print(curr_url)
        
        soup = BeautifulSoup(html, "html.parser")
        
        img = soup.find_all("img", id="mangaFile")
        img_urls = [i["src"] for i in img]

        with requests.Session() as session:
            for idx, i in enumerate(img_urls):
                response = session.get(i, headers={'User-Agent': 'Mozilla/5.0', "referer":f"{curr_url}"})
            
                if response.status_code == 200:
                    
                    with open(f"./imgs/{name}/ch{ch}/pg{pg}-{idx}.jpg", "wb") as f:
                        f.write(response.content)
                        
                else:
                    print("Error", response.reason)

        # go to next page
        status = click_next_page(driver)
        print(status)
        if status == Status.END_OF_CH:
            ch += 1
            pg = 1
            make_comic_dir(name, ch)
        elif status == Status.END_OF_COMIC:
            end = True
        else:
            pg += 1
            
    driver.close()
    
if __name__ == "__main__":
    main()