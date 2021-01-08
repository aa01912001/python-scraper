import json
import requests
from bs4 import BeautifulSoup

def GPU_score(gpu1, gpu2):
	req = requests.get(r"https://benchmarks.ul.com/compare/best-gpus?amount=0&sortBy=SCORE&reverseOrder=false&types=MOBILE,DESKTOP&minRating=0&search=" + gpu1)
	bsObj = BeautifulSoup(req.text, 'html.parser')
	url1 =  bsObj.find('a', {'class':'OneLinkNoTx'})['href'] # find gpu1's url
	
	gpus_dict = dict()
	tmp_dict = dict()
	#tmp_dict['name'] = bsObj.find_all('a', {'class':'OneLinkNoTx'})[0].text

	req = requests.get(url1)
	bsObj = BeautifulSoup(req.text, 'html.parser')
	tmp_dict['score'] = bsObj.find('span', {'class':'result-pimp-badge-score-item'}).text
	tmp_dict['rank'] = bsObj.find_all('div', {'class':'product-information'})[0].find('span', {'class':'score-large'}).text
	tmp_dict['MSRR'] = bsObj.find_all('div', {'class':'product-information'})[0].find('span', {'class':'price-large'}).text.replace(" ", "").replace("\n", "").replace("$", "")
	tmp_dict['DirectX'] = bsObj.find_all('div', {'class':'product-information'})[1].find_all('span', {'class':'score-large'})[0].text
	tmp_dict['TDP'] = bsObj.find_all('div', {'class':'product-information'})[1].find_all('span', {'class':'score-large'})[1].text.replace(" W", "")

	gpus_dict[gpu1] = tmp_dict
	
	if gpu2 != "No suggestion":
		try:
			req = requests.get(r"https://benchmarks.ul.com/compare/best-gpus?amount=0&sortBy=SCORE&reverseOrder=false&types=MOBILE,DESKTOP&minRating=0&search=" + gpu2)
			bsObj = BeautifulSoup(req.text, 'html.parser')
			url1 =  bsObj.find('a', {'class':'OneLinkNoTx'})['href'] # find gpu1's url
			
			tmp_dict = dict()

			req = requests.get(url1)
			bsObj = BeautifulSoup(req.text, 'html.parser')
			tmp_dict['score'] = bsObj.find('span', {'class':'result-pimp-badge-score-item'}).text
			tmp_dict['rank'] = bsObj.find_all('div', {'class':'product-information'})[0].find('span', {'class':'score-large'}).text
			tmp_dict['MSRR'] = bsObj.find_all('div', {'class':'product-information'})[0].find('span', {'class':'price-large'}).text.replace(" ", "").replace("\n", "").replace("$", "")
			tmp_dict['DirectX'] = bsObj.find_all('div', {'class':'product-information'})[1].find_all('span', {'class':'score-large'})[0].text
			tmp_dict['TDP'] = bsObj.find_all('div', {'class':'product-information'})[1].find_all('span', {'class':'score-large'})[1].text.replace(" W", "")

			gpus_dict[gpu2] = tmp_dict
			result_json = json.dumps(gpus_dict, indent=4, separators=(',', ': '), ensure_ascii=False) #  convert dict into json format	
		except Exception as e:
			tmp_dict = dict()
			tmp_dict['score'] = "No data"
			tmp_dict['rank'] = "No data"
			tmp_dict['MSRR'] = "No data"
			tmp_dict['DirectX'] = "No data"
			tmp_dict['TDP'] = "No data"
			gpus_dict[gpu2] = tmp_dict
			result_json = json.dumps(gpus_dict, indent=4, separators=(',', ': '), ensure_ascii=False) #  convert dict into json format	
	else:
		tmp_dict = dict()
		tmp_dict['score'] = ""
		tmp_dict['rank'] = ""
		tmp_dict['MSRR'] = ""
		tmp_dict['DirectX'] = ""
		tmp_dict['TDP'] = ""
		gpus_dict[gpu2] = tmp_dict
		result_json = json.dumps(gpus_dict, indent=4, separators=(',', ': '), ensure_ascii=False) #  convert dict into json format	
	return result_json

	

if __name__ == '__main__':
	# GPU_score("AMD Radeon R9 290", "NVIDIA GeForce RTX 3090")
	pass