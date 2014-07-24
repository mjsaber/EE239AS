from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

with open("links/topic_links") as f:
	urls = f.read().splitlines()
anscsv = open("answers.csv", mode="w")

# links = open("links/questiones", mode='w')

user_set = set()
# record = urls[4]
for record in urls:
	anonymous = 0
	question_links = set()
	url = record.split(',')[0]
	current_topic = record.split(',')[1]
	browser.get(url)
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		src = src_updated
		time.sleep(2)
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		src_updated = browser.page_source
	split_html = src.split("<h3>")
	for i in range(1,len(split_html)):
		part = split_html[i].split('</h3>')[0]
		part_soup = BeautifulSoup(part)
		for link in part_soup.find_all('a' , href=True):
			question_links.add(link['href'])
			# links.write(link['href'].encode('utf-8') + '\n')
	print len(question_links)
	for question in question_links:
		question_url = "http://quora.com" + question + "?share=1"
		browser.get(question_url)
		ans_updated = browser.page_source
		ans = ""
		while ans != ans_updated:
			ans = ans_updated
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			ans_updated = browser.page_source
		more_votes = browser.find_elements_by_css_selector("a[class='more_link']")
		for more_vote in more_votes:
			browser.execute_script("arguments[0].click();", more_vote)
			time.sleep(1)
		src = browser.page_source
		soup = BeautifulSoup(src)
		header = soup.find('h1').parent.parent.parent
		question_text = header.get_text()
		question_id = question.encode('utf-8')
		tags = soup.find_all('div',attrs={"class":"topic_list_item"})
		all_tags = ""
		for i in range(len(tags)):
			if i == 0:
				all_tags = tags[i].get_text().strip()
			else:
				all_tags = all_tags + ', ' + tags[i].get_text().strip()

		answers = soup.find_all(attrs={"class":"answer_wrapper"})
		answered = 0
		answer_id = question_id
		user_id=""
		date=""
		number_of_upvotes=""
		user_upvoted=""
		answer_text=""
		for answer in answers:
			answered = 1
			users = answer.find(attrs={"class":"answer_user_wrapper"})
			link = users.find('a' , href=True)
			if link != None:
				user_id = link['href'].encode('utf-8')
				user_set.add(link['href'])
			else:
				anonymous += 1
				user_id = "anonymous" + str(anonymous)
			answer_id = question_id + '-' + user_id
			number_of_upvotes = answer.parent.find(attrs={"class":"numbers"}).get_text().encode('utf-8')
			voter = answer.find(attrs={"class":"answer_voters"})
			if voter != None:		
				is_voted = 0
				for link in voter.find_all('a', href=True):
					if is_voted == 0:
						user_upvoted = link['href']
						user_set.add(link['href'])
						is_voted = 1
					else:
						user_upvoted = user_upvoted + ", " + link['href']
						user_set.add(link['href'])

			answer_content = answer.find(attrs={"class":"answer_content"})
			answer_text = answer_content.get_text().split("Embed")[0].strip()
			date = answer.find(attrs={"class":"answer_permalink"}).get_text().encode('utf-8')
			date = date.replace(",","")
			data = answer_id+','+question_id+','+ user_id + ','+ date + ','+number_of_upvotes+ ','+ '{{{' + user_upvoted.encode('utf-8') + '}}}' +','+ '{{{' + all_tags.encode('utf-8') + '}}}' +','+ current_topic.encode('utf-8') + ','+'{{{' + question_text.encode('utf-8') + '}}}'+','+ '{{{' + answer_text.encode('utf-8') +'}}}'
			anscsv.write(data + '\n')
		if answered == 0:
			data = answer_id+','+question_id+','+ user_id + ','+ date + ','+number_of_upvotes+ ','+ '{{{' + user_upvoted.encode('utf-8') + '}}}' +','+ '{{{' + all_tags.encode('utf-8') + '}}}' +','+ current_topic.encode('utf-8') + ','+'{{{' + question_text.encode('utf-8') + '}}}'+','+ '{{{' + answer_text.encode('utf-8') +'}}}'

with open("links/user_links", mode='w') as f:
	for url in user_set:
		f.write(url.encode('utf-8') + '\n')
# links.close()
anscsv.close()
