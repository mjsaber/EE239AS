from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

with open("links/user_links") as f:
	urls = f.read().splitlines()
usercsv = open("users.csv", mode="w")
for link in urls:
# link = "/Kim-Bott"
	user_id = link
	url = "http://quora.com" + user_id + "?share=1"
	browser.get(url)
	src = browser.page_source
	soup = BeautifulSoup(src)
	link = open("test", mode='w')
	link.write(soup.prettify().encode('utf-8'))
	info = []
	info_tag = ["Topics","Blogs","Questions","Answers","Edits","Followers","Following"]
	items = soup.find_all('a', attrs={"class":"link_label"})
	for tag in info_tag:
		flag = 0
		for item in items:
			s = item.get_text()
			if tag in s:
				flag = 1
				count = s[len(tag):].strip()
				info.append(count)
		if flag == 0:
			info.append("")

	number_of_topics = info[0].encode('utf-8')
	number_of_blogs = info[1].encode('utf-8')
	number_of_questions = info[2].encode('utf-8')
	number_of_answers = info[3].encode('utf-8')
	number_of_edits = info[4].encode('utf-8')
	followers = ""
	following = ""
	if info[5] != "":
		follower_url = "http://quora.com" + user_id + "/followers?share=1"
		browser.get(follower_url)
		src_updated = browser.page_source
		src = ""
		while src != src_updated:
			src = src_updated
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
			src_updated = browser.page_source
		src = browser.page_source
		soup = BeautifulSoup(src)
		has_follower = 0
		for user in soup.find_all('h2'):
			for link in user.find_all('a' , href=True):
				if has_follower == 0:
					followers = link['href']
					has_follower = 1
				else:
					followers = followers + ", " + link['href']

	if info[6] != "":
		following_url ="http://quora.com" + user_id + "/following?share=1"
		browser.get(following_url)
		src_updated = browser.page_source
		src = ""
		while src != src_updated:
			src = src_updated
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
			src_updated = browser.page_source
		src = browser.page_source
		soup = BeautifulSoup(src)
		has_following = 0
		for user in soup.find_all('h2'):
			for link in user.find_all('a' , href=True):
				if has_following == 0:
					following = link['href']
					has_following = 1
				else:
					following = following + ", " + link['href']
	following = '{{{' + following.encode('utf-8') + '}}}'
	followers = '{{{' + followers.encode('utf-8') + '}}}'
	data = user_id+','+ number_of_topics +','+ number_of_blogs + ','+ number_of_questions + ','+number_of_answers+ ','+ number_of_edits + ','+followers + ',' +following
	usercsv.write(data + '\n')
usercsv.close()
# links.close()
# print list_items.prettify()