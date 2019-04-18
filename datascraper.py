import requests
import re
import csv
from bs4 import BeautifulSoup

#creating a class for easy usage of objects
def CZONE(type,link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content,'html.parser')
	if(soup.find(id="anLastPageBottom").has_attr('href')):
		pages = int(soup.find(id="anLastPageBottom")['href'][-1])
		print(pages)
	else:
		pages = 1
	for page in range(1,pages+1):
		pagelink = link+"?page="+str(page)
		print(pagelink)
		req = requests.get(pagelink)
		soup = BeautifulSoup(req.content, "html.parser")
		for product in range(len(soup.find_all("div",class_="product"))):
			pn='rptListView_ctl0'+str(product)+'_anProductName'
			pn = soup.find(id=pn).text.strip()
			pp='rptListView_ctl0'+str(product)+'_spnPrice'
			pp = soup.find(id=pp).text.strip()
			if(type=='CPU'):
				products.append(CPU(pn,pp))
			elif(type=='MOBO'):
				code=soup.find(id='rptListView_ctl0'+str(product)+'_spnProductCode').text.strip()
				products.append(MOBO(pn,pp,code))

	return products
def PAKDUKAAN(type,link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	pages = len(soup.find_all('ol')[0].find_all('li'))-1
	for page in range(pages):
		pagelink = link+'?p='+str(page+1)
		req = requests.get(pagelink)
		soup = BeautifulSoup(req.content, "html.parser")
		for product in soup.find_all("div",class_="product-item-info"):
			pn=product.find("h2",class_="product-name").a['title'].strip().replace(u"\u2122", '').replace(u"\u00AE",'')
			pp=product.find("span",class_="price").text.strip()
			products.append(CPU(pn,pp))
	return products
def GALAXY(type, link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	pages = len(soup.find("ul",class_="pages-items").find_all("li")[2])-1
	for page in range(pages):
		pagelink = link+"?p="+str(page+1)
		req=requests.get(pagelink)
		soup = BeautifulSoup(req.content,"html.parser")
		productlist = soup.find_all("li",class_="product-item")
		productlist = productlist[1:]
		for product in productlist:
			pn=product.find("a",class_="product-item-link").text.strip()
			pp=product.find("span",class_="price").text
			pp=pp[:-3]
			products.append(CPU(pn,pp))
	return products
def SHINGPOINT(type, link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content,'html.parser')
	if(soup.find(id="anLastPageBottom").has_attr('href')):
		pages = int(soup.find(id="anLastPageBottom")['href'][-1])
	else:
		pages = 1
	for page in range(1,pages+1):
		pagelink = link+"?page="+str(page)
		req = requests.get(pagelink)
		soup = BeautifulSoup(req.content, "html.parser")
		for product in range(len(soup.find_all("div",class_="product"))):
			pn='rptListView_ctl0'+str(product)+'_anProductName'
			
			tempsoup = BeautifulSoup(requests.get("https://www.shingpoint.com.pk"+((soup.find(id=pn))['href'])).content,'html.parser')
			pn = soup.find(id=pn).text.strip()
			pp='rptListView_ctl0'+str(product)+'_spnPrice'
			pp = soup.find(id=pp).text.strip()
			
			code = tempsoup.find(id='spnProductCode').text.strip()
			print(str(product)+'\t'+pn[:10]+'\t'+pp+'\t'+code)
			products.append(MOBO(pn,pp,code))
			

	return products
def MOBOscrap():
	links=['http://czone.com.pk/motherboards-pakistan-ppt.157.aspx','https://www.shingpoint.com.pk/motherboards-pakistan-ppt.10302.aspx']
	CPUS = set()
	czone_prices=CZONE('MOBO',links[0])
	shingpoint_price=SHINGPOINT('MOBO',links[1])
	for product in czone_prices:
		CPUS.add(product)
	for product in shingpoint_price:
		CPUS.add(product)
	return CPUS, czone_prices, shingpoint_price

def CPUscrap():
	links = ['http://czone.com.pk/processors-pakistan-ppt.85.aspx','https://www.pakdukaan.com/pc-hardware-accessories/processors','https://www.galaxy.pk/pc-addons/processor/intel.html']
	CPUs = set()
	czone_prices=CZONE('CPU',links[0])
	pakdukaan_prices=PAKDUKAAN('CPU',links[1])
	galaxy_prices=GALAXY('CPU',links[2])

	for product in czone_prices:
		CPUs.add(product)
	for product in pakdukaan_prices:
		CPUs.add(product)
	for product in galaxy_prices:
		CPUs.add(product)
	return CPUs, czone_prices, pakdukaan_prices, galaxy_prices

class MOBO:
	def __init__(self,name, price,code):
		data = self.normalize(name, price, code)
		self.id = data['id']
		self.title = data['title']
		self.chipset=data['chipset']
		self.vendor=data['vendor']
		self.brand,self.socket=self.getSocket()
		self.price=data['price']
		def __eq__(self, other):
			return self.CPUid == other.CPUid
		def __hash__(self):
			return hash (self.CPUid)	
	def getSocket(self):
		if(self.chipset not in ['X470','X370','B450','B350','A320','X300','A300','B300']):
			if(re.search('[HBQPZ]5[57]$',self.chipset)):
				socket='LGA 1156'
			elif(re.search('[HBQPZ][67][1-8]$',self.chipset)):
				socket='LGA 1155'
			elif(re.search('[HBQPZ][89][1-8]$',self.chipset)):
				socket='LGA 1150'
			elif(re.search('[X][579][8-9]$',self.chipset)):
				socket='LGA 2011'
			elif(re.search('[HBQZ][12][0-9]0$',self.chipset)):
				socket='LGA 1151'
			elif(re.search('[HBQZ][3][0-9]0$',self.chipset)):
				socket='LGA 1151-2'
			else:
				socket='Invalid'
			return 'Intel',socket
		else:
			return 'AMD','AM4'
	def normalize(self,name,price,code):
		data = {}
		data['id']=code.replace(' ','-').replace('(','-').replace(')','-').upper()
		data['title']=name
		data['vendor']=name.split(' ',1)[0]#retrieving the vendor name, which is always at front
		data['chipset']=(re.search(('[AHBQZX]([0-9])+'),name).group(0)) if (re.search(('[AHBQZX]([0-9])+'),name)) else 'not available'
		data['price']=int(price.replace(',','')[3:]) #removing Rs. from 'Rs. 20000'
		return data
		

class CPU:
	def __init__(self,name, price):
		data = self.normalize(name, price)
		self.CPUid = data['id']
		self.CPUtitle = data['title']
		self.CPUbrand = data['brand']
		self.CPUseries = data['series']
		self.CPUgen = data['gen']
		self.CPUunlocked = data['unlocked']
		self.CPUprice = data['price']
		self.CPUsocket, self.CPUcodename = self.getSocket()
	def __eq__(self, other):
		return self.CPUid == other.CPUid
	def __hash__(self):
		return hash (self.CPUid)
	
	def getSocket(self):
		socket = 'None'
		codename = 'None'
		if(self.CPUbrand=='Intel'):
			if(re.search(("2[0-7]{4}"),self.CPUid)):
				socket = 'LGA 1155'
				codename = 'Sandy Bridge'
			elif(re.search(("3[0-7]{4}"),self.CPUid)):
				socket = 'LGA 1155'
				codename = 'Ivy Bridge'
			elif(re.search(("4[0-7]{4}"),self.CPUid)):
				socket = 'LGA 1150'
				codename = 'Haswell'
			elif(re.search(("5[0-7]{4}"),self.CPUid)):
				socket = 'LGA 1150'
				codename = 'Broadwell'
			elif(re.search(("6[0-7]{4}"),self.CPUid)):
				socket = 'LGA 1151'
				codename = 'Skylake'
			elif(re.search(("7[0-7]{4}"),self.CPUid)):
				socket = 'LGA 1151'
				codename = 'Kabylake'
			elif(re.search(("8[0-9]{4}"),self.CPUid)):
				socket = 'LGA 1151-2'
				codename = 'Coffeelake'
			elif(re.search(("9[0-9]{4}"),self.CPUid)):
				socket = 'LGA 1151-2'
				codename = 'Coffeelake'
			elif(re.search(("3[8-9]{4}"),self.CPUid)):
				socket = 'LGA 2011'
				codename = 'Sandy Bridge-E'
			elif(re.search(("4[8-9]{4}"),self.CPUid)):
				socket = 'LGA 2011'
				codename = 'Ivy Bridge-E'
			elif(re.search(("5[8-9]{4}"),self.CPUid)):
				socket = 'LGA 2011'
				codename = 'Haswell-E'
			elif(re.search(("6[8-9]{4}"),self.CPUid)):
				socket = 'LGA 2011'
				codename = 'Broadwell-E'
		else:
			if(re.search(("1[2-9]{3}"),self.CPUid)):
				socket = 'AM4'
				codename = 'Summit Ridge'
			elif(re.search(("2[2-9]{3}"),self.CPUid)):
				socket = 'AM4'
				codename = 'Pinnacle Ridge'
		return socket,codename

	#function to normalize/parse the content of a CPU product title
	def normalize(self,name, price):
		data = {}
		name.replace(',','').replace('Processor','').replace('Desktop','') #removing unrequired tags
		data['id']=(re.search(("[0-9]{4}(K|k|T|t|P|p|U|u|X|x)?"),name).group(0).upper()) #getting the CPU by using regex to find 4 consecutive occurences of numbers eg 8000k
		data['title']=(name) #complete title of the product for descriptive purposes
		data['brand']=(re.search(("(Intel|AMD)"),name).group(0)) #regex to find product brand, amd or intel
		data['series']=(re.search(("(Core|Ryzen)( |-)((i|I)[0-9]|[0-9])"),name).group(0)) #regex to find series e.g Ryzen 5 or Core i7
		data['gen']=(data['id'][0])#getting the generation
		data['id']=data['brand'][0]+data['id'] #appending company initial in the ID, 'A' or 'I' to descriminate intel and amd
		if(data['brand'][0]=='A' or data['id'][-1:]=='K'): #defining the state of overclockability
			data['unlocked']='Yes'
		else:
			data['unlocked']='No'
		data['price']=int(price.replace(',','')[3:]) #removing Rs. from 'Rs. 20000'
		return data
	

	
def main():
	#available_cpus, czone_cpus, pakdukaan_cpus, galaxy_cpus = CPUscrap()
	available_mobos, czone_mobos,shingpoint_mobos = MOBOscrap()
	print('id\tbrand\tvendor\tchipset\tsocket')
	for mobos in czone_mobos:
		print('%-30s %-10s %-10s %-10s %-10s'% (mobos.id, mobos.brand, mobos.vendor, mobos.chipset, mobos.socket))
	print("\n\nSHINGPOINT")
	for mobos in shingpoint_mobos:
		print('%-30s %-10s %-10s %-10s %-10s'% (mobos.id, mobos.brand, mobos.vendor, mobos.chipset, mobos.socket))
	with open('shingpoint_mobos.csv',mode='w') as csv_file:
		writer = csv.writer(csv_file,delimiter=',')
		for mobo in shingpoint_mobos:
			writer.writerow([mobo.id, mobo.brand, mobo.vendor, mobo.chipset, mobo.socket,mobo.price])
	with open('czone_mobos.csv',mode='w') as csv_file:
		writer = csv.writer(csv_file,delimiter=',')
		for mobo in czone_mobos:
			writer.writerow([mobo.id, mobo.brand, mobo.vendor, mobo.chipset, mobo.socket,mobo.price])

	#for avail in available_cpus:
	#	print(avail.CPUid)
	
	"""with open('available_cpus.csv', mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for CPU in available:
			writer.writerow([CPU.CPUid,CPU.CPUbrand,CPU.CPUtitle,CPU.CPUseries,CPU.CPUgen,CPU.CPUcodename,CPU.CPUsocket,CPU.CPUunlocked])
	with open('czone_cpus.csv', mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for CPU in czone_cpus:
			writer.writerow([CPU.CPUid,CPU.CPUprice])
	with open('pakdukaan_cpus.csv', mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for CPU in pakdukaan_cpus:
			writer.writerow([CPU.CPUid,CPU.CPUprice])
	with open('galaxy_cpus.csv', mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for CPU in galaxy_cpus:
			writer.writerow([CPU.CPUid,CPU.CPUprice])"""

if __name__ == "__main__":
	main()

