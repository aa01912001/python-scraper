import requests
import json
import urllib
import time
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def search_by_name(name):
	
	req = requests.get(r'https://store.steampowered.com/search/?term=' + name)
	bsObj = BeautifulSoup(req.text, 'html.parser')
	game_list = bsObj.find('div', {'id':'search_resultsRows'}).find_all('a') #  game list
	game_dict = dict() # it's gonnna convert into json 

	for item in game_list:
		tmp_dict = dict()
		
		name = item.find('span', {'class':'title'}).text
		tmp_dict['title'] = name
		tmp_dict['date'] = item.find('div', {'class':'search_released'}).text #  find game release date
		price = item.find('div', {'class':'search_price'}).text.strip() #  find game price
		if price == "":
			price = "None"

		if price.count("NT") >= 2:
			price = price[price[2:].find('NT')+2:]
		tmp_dict['price'] = price.replace(",", "")
		tmp_dict['url'] = item.find('img')['src'] #  find image url

		try:
			tmp_dict['db_id'] = item['data-ds-appid'] # data base ID
		except:
			tmp_dict['db_id'] = 'None' # some games have no db_id

		tmp_dict['link_url'] = item['href'] #  find link url
		game_dict[name] = tmp_dict

	# for i in game_dict:
	# 	print(game_dict[i])

	result_json = json.dumps(game_dict, indent=4, separators=(',', ': '), ensure_ascii=False) #  convert dict into json format
	return result_json

def search_history_price(name, db_id):
	header_info = { #  header information
		'authority': "steandb.info",
		'path': "/api/GetPriceHistory/?appid='" + db_id + "'&cc=tw",
		'method' : "GET",
		'scheme': "https",
		'accept': "application/json, text/javascript, */*; q=0.01",
		# 'accept-encoding' : "gzip, deflate, br",
		# 'accept-language' : "zh-TW,zh;q=0.9,en-US",
		# 'cookie' : "__cfduid=daa908c7ca691913607d4bdefddeaee101606985634; _ga=GA1.2.1175459012.1606986019; _gid=GA1.2.411580030.1606986019",
		'referer': "https://steamdb.info/app/" + db_id + "/",
		'sec-fetch-dest' : "empty",
		'sec-fetch-mode' : "cors",
		'sec-fetch-site' : "same-origin",
		'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		'x-requested-with' : "XMLHttpRequest"


	}

	req = requests.get(r'https://steamdb.info/api/GetPriceHistory/?appid=' + db_id + '&cc=tw', headers=header_info) # // get price history
	price_history_dict = json.loads(req.text) # convert dict string to dict
	 
	price_history_dict_clean = dict()
	price_history_list = list()
	count = 0
	for history in price_history_dict['data']['history']:
		tmp = dict()
		timeStamp = history['x']/1000
		timeArray = time.localtime(timeStamp)
		otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
		tmp['date'] = otherStyleTime #  update date
		tmp['price'] = history['f'][4:] #  price (NT)
		tmp['discount'] = history['d'] #  discount ratio
		tmp['timestamp'] = timeStamp
		tmp['month'] = time.strftime("%m", timeArray)
		if(int(tmp['discount']) == 0) :
			tmp['month'] = "-1"
		# price_history_list.append(tmp)
		price_history_dict_clean[str(count)] = tmp
		count += 1
	# price_history_dict_clean[name] = price_history_list

	result_json = json.dumps(price_history_dict_clean, indent=4, separators=(',', ': '), ensure_ascii=False) #  convert dict into json format
	
	#print(result_json)

	return result_json

def search_game_info(name, link):
	req = requests.get(link)
	bsObj = BeautifulSoup(req.text, 'html.parser')
	game_info_dict = dict() # it's gonnna convert into json 
	tmp_dict = dict()

	tmp_dict['title'] = bsObj.find('div', {'class':'apphub_AppName'}).text
	tmp_dict['release_date'] = bsObj.find('div', {'class':'date'}).text

	pro = ""
	ram = ""
	gpu = ""
	if bsObj.find('div', {'class':'game_area_sys_req_full'}) is not None : #  只有最低配備
		print(bsObj.find('div', {'class':'game_area_sys_req_full'}).find('ul', {'class':'bb_ul'}))
		for item in bsObj.find('div', {'class':'game_area_sys_req_full'}).find('ul', {'class':'bb_ul'}):
			if item.find('strong').text == "Processor:":
				pro = item.text.replace("Processor:","").lstrip()

			if item.find('strong').text == "Memory:":
				ram = item.text.replace("Memory:","").lstrip()
				
			
			if item.find('strong').text == "Graphics:":
				gpu = item.text.replace("Graphics:","").lstrip()

			if item.find('strong').text == "Video:":
				gpu = item.text.replace("Video:","").lstrip()
	else : #  建議配備
		for item in bsObj.find('div', {'class':'game_area_sys_req_rightCol'}).find('ul', {'class':'bb_ul'}):
			if(item.find('strong') is None):
				continue
			if item.find('strong').text == "Processor:":
				pro = item.text.replace("Processor:","").lstrip()

			if item.find('strong').text == "Memory:":
				ram = item.text.replace("Memory:","").lstrip()
				
			
			if item.find('strong').text == "Graphics:":
				gpu = item.text.replace("Graphics:","").lstrip()

			if item.find('strong').text == "Video:":
				gpu = item.text.replace("Video:","").lstrip()
			
	tmp_dict['processor'] = pro
	tmp_dict['ram'] = ram
	tmp_dict['gpu'] = gpu.split(", ")[0].split(" / ")[0].split(" or ")[0].split(" | ")[0]

	t = ""
	if(len(re.findall("\dG",tmp_dict['gpu'])) > 0):
		t = re.findall("\dG",tmp_dict['gpu'])[0]
	tmp_dict['gpu'] = re.sub(" \dG", "-"+t, tmp_dict['gpu'])
	tmp_dict['gpu'] = re.sub(r'[^a-zA-Z\-\ \d]', '', tmp_dict['gpu'])
	tmp_dict['gpu'] = re.sub(r'-\dGB', '', tmp_dict['gpu'])

	tmp_dict['url'] = bsObj.find('img', {'class':'game_header_image_full'})['src']

	game_info_dict[name] = tmp_dict
	
	result_json = json.dumps(game_info_dict, indent=4, separators=(',', ': '), ensure_ascii=False) #  convert dict into json format
	return result_json


if __name__ == '__main__':
	
	search_game_info("Warframe" ,r"https://store.steampowered.com/app/1172470/Apex/")
	
	#search_history_price("Mirror", "644560")



	#search_by_name("mirror")