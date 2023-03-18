import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

driver = webdriver.Chrome()
driver.get('https://www.factcheck.org/')

driver.implicitly_wait(20)


# get news' information
def get_news():
    with open('FactCheck.csv', mode='a', encoding='utf-8', newline='') as f:
        write = csv.writer(f)
        driver.implicitly_wait(5)
        imges = driver.find_elements(By.CSS_SELECTOR, '#wrapper-index article div.row')
        rows = driver.find_elements(By.CSS_SELECTOR, '#wrapper-index article h3')
        for i in range(0, len(rows)):
            row = rows[i]
            img_row = imges[i]
            # get img url
            # if the img exists, just get, if not, save null
            try:
                img_row.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                print("Img exists")
                img = img_row.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            except selenium.common.exceptions.NoSuchElementException:
                print("Img doesn't exist")
                img = ''
            # img = row.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            # get a news url

            news_url = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            # news_url = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            driver.get(news_url)
            driver.implicitly_wait(5)
            # time.sleep(5)
            # get this news' title
            title = driver.find_element(By.CSS_SELECTOR, '.entry-title').text
            # get this news' author
            author = driver.find_element(By.CSS_SELECTOR, '.byline a').text
            # get this news' post date
            date = driver.find_element(By.CSS_SELECTOR, '.posted-on').text
            # get this news' content
            data = driver.find_elements(By.CSS_SELECTOR, '.entry-content:nth-child(1) p')
            content = []
            for li in data:
                content.append(li.text)
            print(title, "--------", author, "--------", date, "--------", img, "--------", content)
            all_news = [title, author, date, img, content]
            write.writerow(all_news)
            # After saving this news information, get back to the home page, then we can get next news.
            driver.back()
            time.sleep(1)


# find next page
def next_page():
    # driver.find_element(By.LINK_TEXT, 'Next page').click()
    # driver.find_element(By.CSS_SELECTOR, '#wrapper-index nav span').click()
    driver.find_element(By.CSS_SELECTOR, '#wrapper-index nav li.page-item-next span').click()


if __name__ == '__main__':
    for i in range(1, 368):
        js_all = 'document.documentElement.scrollTop = document.documentElement.scrollHeight'  # roll down
        driver.execute_script(js_all)
        print("Page" + str(i))
        get_news()
        next_page()

input()
driver.quit()






