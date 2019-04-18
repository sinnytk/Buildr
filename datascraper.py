import requests
import re
import config #contains the details for the database connection
import csv
import mysql.connector
from bs4 import BeautifulSoup

#creating a class for easy usage of objects
def CZONE(type,link):
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
		print("Scraping CZONE for "+type+" on page: "+str(page))
		soup = BeautifulSoup(req.content, "html.parser")
		for product in range(len(soup.find_all("div",class_="product"))):
			pn='rptListView_ctl0'+str(product)+'_anProductName'
			pl="https://www.czone.com.pk"+soup.find(id=pn)['href']
			pn = soup.find(id=pn).text.strip()
			pp='rptListView_ctl0'+str(product)+'_spnPrice'
			pp = soup.find(id=pp).text.strip()
			if(type=='CPU'):
				products.append(CPU(pn,pp,pl))
			elif(type=='MOBO'):
				code=soup.find(id='rptListView_ctl0'+str(product)+'_spnProductCode').text.strip()
				products.append(MOBO(pn,pp,code,pl))

	return products
def PAKDUKAAN(type,link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	pages = len(soup.find_all('ol')[0].find_all('li'))-1
	for page in range(1,pages+1):
		pagelink = link+'?p='+str(page)
		req = requests.get(pagelink)
		print("Scraping PAKDUKAAN for "+type+" on page: "+str(page))
		soup = BeautifulSoup(req.content, "html.parser")
		for product in soup.find_all("div",class_="product-item-info"):
			p=product.find("h2",class_="product-name")
			pl=p.a['href']
			pn=p.a['title'].strip().replace(u"\u2122", '').replace(u"\u00AE",'')
			pp=product.find("span",class_="price").text.strip()
			products.append(CPU(pn,pp,pl))
	return products
def GALAXY(type, link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	pages = len(soup.find("ul",class_="pages-items").find_all("li")[2])-1
	for page in range(1,pages+1):
		pagelink = link+"&p="+str(page)
		req=requests.get(pagelink)
		print("Scraping GALAXY for "+type+" on page: "+str(page))
		soup = BeautifulSoup(req.content,"html.parser")
		productlist = soup.find_all("li",class_="product-item")
		productlist=productlist[1:]
		for product in productlist:
			p=product.find("a",class_="product-item-link")
			pl=p['href']
			pn=p.text.strip()
			pp=product.find("span",class_="price").text
			pp=pp[:-3]
			products.append(CPU(pn,pp,pl))
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
		print("Scraping SHINGPOINT for "+type+" on page: "+str(page))
		soup = BeautifulSoup(req.content, "html.parser")
		for product in range(len(soup.find_all("div",class_="product"))):
			pn='rptListView_ctl0'+str(product)+'_anProductName'
			pl="https://www.shingpoint.com.pk"+(soup.find(id=pn))['href']
			tempsoup = BeautifulSoup((requests.get(pl)).content,'html.parser')
			pn = soup.find(id=pn).text.strip()
			pp='rptListView_ctl0'+str(product)+'_spnPrice'
			pp = soup.find(id=pp).text.strip()
			code = tempsoup.find(id='spnProductCode').text.strip()
			products.append(MOBO(pn,pp,code,pl))
	return products
def MOBOscrap():
	links=['http://czone.com.pk/motherboards-pakistan-ppt.157.aspx','https://www.shingpoint.com.pk/motherboards-pakistan-ppt.10302.aspx']
	MOBOs = set()
	czone_prices=CZONE('MOBO',links[0])
	shingpoint_price=SHINGPOINT('MOBO',links[1])
	for product in czone_prices:
		MOBOs.add(product)
	for product in shingpoint_price:
		MOBOs.add(product)
	return MOBOs, czone_prices, shingpoint_price

def CPUscrap():
	links = ['http://czone.com.pk/processors-pakistan-ppt.85.aspx','https://www.pakdukaan.com/pc-hardware-accessories/processors','https://www.galaxy.pk/pc-addons.html?cat=1276']
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
	def __init__(self,name, price,code,link):
		data = self.normalize(name, price, code)
		self.id = data['id'].upper()
		self.title = data['title'].upper()
		self.chipset=data['chipset'].upper()
		self.link=link
		self.vendor=data['vendor'].upper()
		self.brand,self.socket=self.getSocket()
		self.price=data['price']
	def __eq__(self, other):
			return self.id == other.id
	def __hash__(self):
			return hash(self.id)
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
				socket='NA'
			return 'INTEL',socket
		else:
			return 'AMD','AM4'
	def normalize(self,name,price,code):
		data = {}
		data['id']=code.replace('-','').replace(' ','-').replace('(','-').replace(')','-').upper()
		data['title']=name
		data['vendor']=name.split(' ',1)[0]#retrieving the vendor name, which is always at front
		data['chipset']=(re.search(('[AHBQZX]([0-9])+'),name).group(0)) if (re.search(('[AHBQZX]([0-9])+'),name)) else 'not available'
		data['price']=int(price.replace(',','')[3:]) #removing Rs. from 'Rs. 20000'
		return data
		

class CPU:
	def __init__(self,name, price,link):
		data = self.normalize(name, price)
		self.id = data['id'].upper()
		self.title = data['title'].upper()
		self.brand = data['brand'].upper()
		self.series = data['series'].upper()
		self.gen = data['gen'].upper()
		self.unlocked = data['unlocked'].upper()
		self.price = data['price']
		self.link=link
		self.socket, self.codename = self.getSocket()
	def __eq__(self, other):
		return self.id == other.id
	def __hash__(self):
		return hash(self.id)
	
	def getSocket(self):
		socket = 'NA'
		codename = 'NA'
		if(self.brand=='INTEL'):
			if(re.search(("2[0-7]{4}"),self.id)):
				socket = 'LGA 1155'
				codename = 'Sandy Bridge'
			elif(re.search(("3[0-7]{4}"),self.id)):
				socket = 'LGA 1155'
				codename = 'Ivy Bridge'
			elif(re.search(("4[0-7]{4}"),self.id)):
				socket = 'LGA 1150'
				codename = 'Haswell'
			elif(re.search(("5[0-7]{4}"),self.id)):
				socket = 'LGA 1150'
				codename = 'Broadwell'
			elif(re.search(("6[0-7]{4}"),self.id)):
				socket = 'LGA 1151'
				codename = 'Skylake'
			elif(re.search(("7[0-7]{4}"),self.id)):
				socket = 'LGA 1151'
				codename = 'Kabylake'
			elif(re.search(("8[0-9]{4}"),self.id)):
				socket = 'LGA 1151-2'
				codename = 'Coffeelake'
			elif(re.search(("9[0-9]{4}"),self.id)):
				socket = 'LGA 1151-2'
				codename = 'Coffeelake'
			elif(re.search(("3[8-9]{4}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Sandy Bridge-E'
			elif(re.search(("4[8-9]{4}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Ivy Bridge-E'
			elif(re.search(("5[8-9]{4}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Haswell-E'
			elif(re.search(("6[8-9]{4}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Broadwell-E'
		else:
			if(re.search(("1[2-9]{3}"),self.id)):
				socket = 'AM4'
				codename = 'Summit Ridge'
			elif(re.search(("2[2-9]{3}"),self.id)):
				socket = 'AM4'
				codename = 'Pinnacle Ridge'
		return socket.upper(),codename.upper()

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
	dbconn=mysql.connector.connect(
		host=config.host,
		user=config.user,
		passwd=config.passwd,
		database=config.database
	)

	available_cpus, czone_cpus, pakdukaan_cpus, galaxy_cpus = CPUscrap()
	available_mobos, czone_mobos,shingpoint_mobos = MOBOscrap()
	try:
		dbconn=mysql.connector.connect(
		host=config.host,
		user=config.user,
		passwd=config.passwd,
		database=config.database
		)
		#id, brand, desc, series, gen, socket, codename, unlocked for CPU
		#id,brand,title,chipset,vendor,socket for MOBO
		CPUdata = []
		MOBOdata = []
		for cpu in available_cpus:
			
			CPUdata.append(tuple((cpu.id,cpu.brand,cpu.title,cpu.series,cpu.gen,cpu.socket,cpu.codename,cpu.unlocked)))
		for mobo in available_mobos:
			MOBOdata.append(tuple((mobo.id,mobo.brand,mobo.title,mobo.chipset,mobo.vendor,mobo.socket)))
		
		CPUquery="INSERT INTO processor values(%s, %s, %s, %s, %s, %s, %s, %s)"
		MOBOquery="INSERT INTO motherboard values(%s, %s, %s, %s, %s, %s)"
		cursor = dbconn.cursor(prepared=True)
		result = cursor.executemany(CPUquery,CPUdata)
		#print(cursor.rowcount() + " records inserted into processor")
		result = cursor.executemany(MOBOquery,MOBOdata)
		dbconn.commit()
		#print(cursor.rowcount()+ "records inserted into motherboard")
	except mysql.connector.Error as error:
		print("Fail {}".format(error))
	finally:
		if(dbconn.is_connected()):
			cursor.close()
			dbconn.close()

if __name__ == "__main__":
	main()

