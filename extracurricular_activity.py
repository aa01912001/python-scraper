"""to find TKU extracurricular activitys newest news
"""
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver


def store_mysql(title_clear_list, info_clear_list, url_clear_list):
    """store extracurricular activity data into mysql"""
    connection = pymysql.connect(host='127.0.0.1', user="root", passwd="zz01912001", db="mysql", charset='utf8')
    cur = connection.cursor()
    cur.execute("USE extracurricular_activity")
    cur.execute("TRUNCATE TABLE title")
    cur.connection.commit()
    for item_title, item_info, item_url in zip(title_clear_list, info_clear_list, url_clear_list):
        cur.execute("INSERT INTO title (title, info, url) VALUES (\"%s\", \"%s\", \"%s\")", (item_title, item_info, item_url))
        cur.connection.commit()
    cur.close()
    connection.close()


def main():
    """main function"""
    driver = webdriver.PhantomJS()
    driver.get("http://spirit.tku.edu.tw/tku/main.jsp?sectionId=3")
    driver.switch_to.frame("MainFrame")  # switch to html iframe section
    bsobj = BeautifulSoup(driver.find_element_by_tag_name("tbody").get_attribute("outerHTML"), "html.parser")
    article_list = bsobj.find_all("tbody")[2].find_all("td", {"class": "MasterTableCell"})
    title_clear_list = []
    info_clear_list = []
    url_clear_list = []
    for item in article_list:
        title_clear_list.append(item.a.text)
        info_clear_list.append(item.span.span.text)
        url_clear_list.append("http://spirit.tku.edu.tw/tku/" + item.a['href'])
        print("{} {} http://spirit.tku.edu.tw/tku/{}".format(item.a.text, item.span.span.text, item.a['href']))
    store_mysql(title_clear_list, info_clear_list, url_clear_list)
    driver.close()
if __name__ == "__main__":
    main()
