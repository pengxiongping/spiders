import requests
from selenium import webdriver
import time
from lxml import etree

header = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

# with open('./login.html','wb') as f:
# 	f.write(res.encode('utf-8'))
# selector = etree.HTML(res)
# user = selector.xpath("//input[@class='btn btn_green btn_active btn_block btn_lg'][1]/@value")

# print(user)

browser = webdriver.Chrome()
browser.get("https://passport.lagou.com/login/login.html")

account = input("请输入用户名：")
password = input("请输入您的密码：")
browser.find_element_by_xpath("//div[@data-view='passwordLogin']/form/div[@data-propertyname='username']/input").clear()

browser.find_element_by_xpath("//div[@data-view='passwordLogin']/form/div[@data-propertyname='username']/input").send_keys(account)
browser.find_element_by_xpath("//div[@data-view='passwordLogin']/form/div[@data-propertyname='password']/input").clear()
browser.find_element_by_xpath("//div[@data-view='passwordLogin']/form/div[@data-propertyname='password']/input").send_keys(password)
browser.find_element_by_xpath("//input[@class='btn btn_green btn_active btn_block btn_lg'][1]").click()
time.sleep(3)


cookie_list = browser.get_cookies()
cookies = {}
for cookie in cookie_list:
	cookies[cookie['name']]= cookie['value']
browser.close()
browser.quit()

res = requests.get("https://www.lagou.com/",headers=header,cookies=cookies).text
with open('./login.html','wb') as f:
	f.write(res.encode('utf-8'))
