from selenium import webdriver
from bs4 import BeautifulSoup
import os

def write_hierarchy(s, url, s_u):
	url = url.split('?')[0] + "/about?share=1"
	browser.get(url)
	src = browser.page_source
	soup = BeautifulSoup(src)
	item = soup.find(text="Child Topics")
	if item == None:
		return
	else:
		item = item.parent.parent
		subtopics = item.find_all('a')
		for t in subtopics:
			url = 'http://www.quora.com' + t['href']
			fw.write(s + '\t' + t.get_text() + '\n')
			fw2.write(s_u + '\t' + url + "?share=1" + '\n')
			fw3.write(url + "?share=1" +',' + t.get_text()+ '\n')
			write_hierarchy(s+ '\t' + t.get_text(), url, s_u+'\t' + url + "?share=1" + '\n')

url = 'http://www.quora.com/Anxiety?share=1'
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

s = "Anxiety"
fw = open("topic_names.txt" , mode='w')
fw2 = open("topic_urls.txt" , mode='w')
fw3 = open("links/topic_links", mode='w')
fw.write(s + '\n')
fw2.write(url + '\n')
fw3.write(url +',Anxiety'+ '\n')

write_hierarchy(s, url, url)

fw.close()
fw2.close()
fw3.close()