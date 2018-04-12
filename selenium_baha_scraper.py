"""2018/1/8"""
import os
import sys
import colorama
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_title_url_content(driver):
    """find out title and its url"""
    title_data = driver.find_elements(By.XPATH, "//a[@class='b-list__main__title']")  # 使用xpath查找title
    for title in title_data:
        print(title.text, '  ', end='')
        url_text = title.get_attribute('href')  # 在firefox driver 上會 return 完整的 URL

        '''There's been a decent amount of debate around this.  For consistency amongst all the
        browsers, we decided to return the fully qualified URL.  This change just hasn't made
        it into the ChromeDriver yet.
        '''
        # relative_url_text = re.sub('https://forum.gamer.com.tw/', '', url_text)
        print(Fore.YELLOW + Style.BRIGHT + url_text)
        print(Style.RESET_ALL)
        get_title_content(url_text)


def get_title_content(title_url):
    """find out first content of title'url"""
    firefox_driver2 = webdriver.Firefox()
    firefox_driver2.get(title_url)
    content = firefox_driver2.find_element(By.CLASS_NAME, 'c-article__content')
    print(Fore.CYAN + Style.BRIGHT + content.text)

    print(Style.RESET_ALL)

    firefox_driver2.close()


if __name__ == '__main__':  # 如果當前模組為主程式則執行下列片段


    try:
        pages = int(sys.argv[1])  # 共要找幾頁
    except:
        print('請記得輸入命令列引數')
        os.system('pause')
        sys.exit('sorry goodbye!')


    if pages <= 0:
        print('命令列引數須為正整數')
        os.system('pause')
        sys.exit('sorry goodbye!')

    """init() will filter ANSI escape sequences out of any text sent to stdout or stderr,
    and replace them with equivalent Win32 calls.
    """
    colorama.init()



    firefox_driver = webdriver.Firefox()
    firefox_driver.get('https://forum.gamer.com.tw/B.php?bsn=60076')#進入場外第一頁
    get_title_url_content(firefox_driver)
    for i in range(2, pages + 1):
        next_url = 'https://forum.gamer.com.tw/B.php?' + 'page=' + str(i) + '&bsn=60076' #第二頁的url
        firefox_driver.get(next_url)
        get_title_url_content(firefox_driver)

    firefox_driver.close()
