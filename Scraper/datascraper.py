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
			pi='rptListView_ctl0'+str(product)+'_imgProduct'
			pl="https://www.czone.com.pk"+soup.find(id=pn)['href']
			pn = soup.find(id=pn).text.strip()
			pp='rptListView_ctl0'+str(product)+'_spnPrice'
			pp = soup.find(id=pp).text.strip()
			pi="https://czone.com.pk"+soup.find(id=pi)['src']
			code=soup.find(id='rptListView_ctl0'+str(product)+'_spnProductCode').text.strip()
			if(type=='CPU'):
				products.append(CPU(pn,pp,pl,pi,"CZONE"))
			elif(type=='MOBO'):
				products.append(MOBO(pn,pp,code,pl,pi,"CZONE"))
			elif(type=="GPU"):
				products.append(GPU(pn,pp,code,pl,pi,"CZONE"))
			elif(type=="RAM"):
				products.append(RAM(pn,pp,code,pl,pi,"CZONE"))


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
			pi=product.img['src']
			if(type=="CPU"):
				products.append(CPU(pn,pp,pl,pi,"PAKDUKAAN"))
			elif(type=="GPU"):
				tempsoup = BeautifulSoup((requests.get(pl)).content,'html.parser')
				code=tempsoup.find("h3",class_="product-shop-sku").strong.text.strip()
				products.append(GPU(pn,pp,code,pl,pi,"PAKDUKAAN"))
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
			pi=product.img['src']
			p=product.find("a",class_="product-item-link")
			pl=p['href']
			pn=p.text.strip()
			pp=product.find("span",class_="price").text
			pp=pp[:-3]
			products.append(CPU(pn,pp,pl,pi,"GALAXY"))
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
			pi='rptListView_ctl0'+str(product)+'_imgProduct'
			pi="https://shingpoint.com.pk"+soup.find(id=pi)['src']
			if(type=="MOBO"):
				products.append(MOBO(pn,pp,code,pl,pi,"SHINGPOINT"))
			elif(type=="GPU"):
				products.append(GPU(pn,pp,code,pl,pi,"SHINGPOINT"))
			elif(type=="RAM"):
				products.append(RAM(pn,pp,code,pl,pi,"SHINGPOINT"))
	return products
def MOBOscrap():
	links=['http://czone.com.pk/motherboards-pakistan-ppt.157.aspx','https://www.shingpoint.com.pk/motherboards-pakistan-ppt.10302.aspx']
	distinct = set()
	_all = []
	czone_prices=CZONE('MOBO',links[0])
	shingpoint_prices=SHINGPOINT('MOBO',links[1])
	for product in czone_prices:
		_all.append(product)
		distinct.add(product)
	for product in shingpoint_prices:
		_all.append(product)
		distinct.add(product)
	return distinct, _all
def RAMscrap():
	distinct=set()
	_all = []
	links = ['http://czone.com.pk/memory-module-ram-desktop-ddr4-memory-pakistan-pt.383.aspx','https://www.shingpoint.com.pk/memory-modules-desktop-ddr3-pakistan-pt.10483.aspx','https://www.shingpoint.com.pk/memory-modules-desktop-ddr4-pakistan-pt.19052.aspx','https://www.shingpoint.com.pk/memory-modules-gaming-ddr3-pakistan-pt.22933.aspx','https://www.shingpoint.com.pk/memory-modules-gaming-ddr4-pakistan-pt.19909.aspx']
	czone_prices=CZONE('RAM',links[0])
	shingpoint_prices=SHINGPOINT('RAM',links[1])
	shingpoint_prices.extend(SHINGPOINT('RAM',links[2]))
	shingpoint_prices.extend(SHINGPOINT('RAM',links[3]))
	shingpoint_prices.extend(SHINGPOINT('RAM',links[4]))
	for product in czone_prices:
		_all.append(product)
		distinct.add(product)
	for product in shingpoint_prices:
		_all.append(product)
		distinct.add(product)
	return distinct, _all
def CPUscrap():
	links = ['http://czone.com.pk/processors-pakistan-ppt.85.aspx','https://www.pakdukaan.com/pc-hardware-accessories/processors','https://www.galaxy.pk/pc-addons.html?cat=1276']
	distinct = set()
	_all = []
	czone_prices=CZONE('CPU',links[0])
	pakdukaan_prices=PAKDUKAAN('CPU',links[1])
	galaxy_prices=GALAXY('CPU',links[2])

	for product in czone_prices:

		_all.append(product)
		distinct.add(product)
	for product in pakdukaan_prices:
		_all.append(product)
		distinct.add(product)
	for product in galaxy_prices:
		_all.append(product)
		distinct.add(product)
	return distinct, _all
def GPUscrap():
	links = ['http://czone.com.pk/graphic-cards-pakistan-ppt.154.aspx','https://www.pakdukaan.com/pc-hardware-accessories/graphics-cards','https://www.shingpoint.com.pk/graphic-cards-pakistan-ppt.10293.aspx']
	distinct = set()
	_all = []
	czone_prices=CZONE('GPU',links[0])
	pakdukaan_prices=PAKDUKAAN('GPU',links[1])
	shingpoint_prices=SHINGPOINT('GPU',links[2])

	for product in czone_prices:
		if(product.id!=''):
			_all.append(product)
			distinct.add(product)
	for product in pakdukaan_prices:
		_all.append(product)
		distinct.add(product)
	for product in shingpoint_prices:
		_all.append(product)
		distinct.add(product)
	return distinct, _all

class MOBO:
	def __init__(self,name, price,code,link,image,seller):
		data = self.normalize(name, price, code)
		self.id = data['id'].upper()
		self.image=image
		self.seller=seller
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
		data['id']=''.join(c for c in code if c.isalnum())
		data['id']=data['id'].upper()
		data['title']=name
		data['vendor']=name.split(' ',1)[0]#retrieving the vendor name, which is always at front
		data['chipset']=(re.search(('[AHBQZX]([0-9])+'),name).group(0)) if (re.search(('[AHBQZX]([0-9])+'),name)) else 'not available'
		data['price']=int(price.replace(',','')[3:]) #removing Rs. from 'Rs. 20000'
		return data
class RAM:
	def __init__(self,name,price,code,link,image,seller):
		data = self.normalize(name, price, code)
		self.id = data['id'].upper()
		self.title = data['title'].upper()
		self.brand = data['brand']
		self.image=image
		self.seller=seller
		self.price = data['price']
		self.speed = data['speed']
		self.rate = data['rate']
		self.size = data['size']
		self.link = link
	def __eq__(self, other):
		return self.id == other.id
	def __hash__(self):
		return hash(self.id)
	def normalize(self,name,price,code):
		data = {}
		data['price']=int(price.replace(',','')[3:])
		data['id']=''.join(c for c in code if c.isalnum())
		data['title']=name
		data['brand']=name.split(' ',1)[0]
		data['speed'] = re.search(('[0-9]{4}'),name).group(0) + 'mhz'
		data['rate'] = re.search(('(DDR)( )?[34]{1}'),name).group(0)
		data['size'] = re.search((' [0-9]{1,2}( )?(gb|GB)'),name).group(0).replace(' ','')
		return data

class GPU:
	def __init__(self,name,price,code,link,image,seller):
		data = self.normalize(name, price, code)
		self.id = data['id'].upper()
		self.image=image
		self.seller=seller
		self.title = data['title'].upper()
		self.brand = data['brand']
		self.vendor = data['vendor'].upper()
		self.price = data['price']
		isGPU = re.search(('((G|R)T(X)? [0-9]{3,})|(RX [0-9]{3})'),name)
		isGPUid = re.search(('((G|R)T(X)?[0-9]{3,})|(RX[0-9]{3})'),self.id)
		if(isGPU):
			self.model=(re.search(('((G|R)T(X)? [0-9]{3,}(TI)?)|(RX [0-9]{3})'),name).group(0)) .replace(' ','')
		elif(isGPUid):
			self.model=(re.search(('((G|R)T(X)?[0-9]{3,}(TI)?)|(RX[0-9]{3})'),self.id).group(0))
		else:
			self.model='NA'
		self.link=link
	def __eq__(self, other):
		return self.id == other.id
	def __hash__(self):
		return hash(self.id)
	def normalize(self,name,price,code):
		data = {}
		data['price']=int(price.replace(',','')[3:])
		data['id']=''.join(c for c in code if c.isalnum())
		data['id']=data['id'][:40]
		data['title']=name
		data['vendor']=name.split(' ',1)[0]
		data['brand'] = 'AMD' if re.search('RX [0-9]{3}',data['title']) else 'NVIDIA'
		return data

class CPU:
	def __init__(self,name, price,link,image,seller):
		data = self.normalize(name, price)
		self.id = data['id'].upper()
		self.image=image
		self.seller=seller
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
		if self.brand=='INTEL':
			if(re.search(("2[0-9]{3}"),self.id)):
				socket = 'LGA 1155'
				codename = 'Sandy Bridge'
			elif(re.search(("3[0-9]{3}"),self.id)):
				socket = 'LGA 1155'
				codename = 'Ivy Bridge'
			elif(re.search(("4[0-9]{3}"),self.id)):
				socket = 'LGA 1150'
				codename = 'Haswell'
			elif(re.search(("5[0-9]{3}"),self.id)):
				socket = 'LGA 1150'
				codename = 'Broadwell'
			elif(re.search(("6[0-9]{3}"),self.id)):
				socket = 'LGA 1151'
				codename = 'Skylake'
			elif(re.search(("7[0-9]{3}"),self.id)):
				socket = 'LGA 1151'
				codename = 'Kabylake'
			elif(re.search(("8[0-9]{3}"),self.id)):
				socket = 'LGA 1151-2'
				codename = 'Coffeelake'
			elif(re.search(("9[0-9]{3}"),self.id)):
				socket = 'LGA 1151-2'
				codename = 'Coffeelake'
			elif(re.search(("3[0-9]{3}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Sandy Bridge-E'
			elif(re.search(("4[0-9]{3}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Ivy Bridge-E'
			elif(re.search(("5[0-9]{3}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Haswell-E'
			elif(re.search(("6[0-9]{3}"),self.id)):
				socket = 'LGA 2011'
				codename = 'Broadwell-E'
		else:
			if(re.search(("1[0-9]{3}"),self.id)):
				socket = 'AM4'
				codename = 'Summit Ridge'
			elif(re.search(("2[0-9]{3}"),self.id)):
				socket = 'AM4'
				codename = 'Pinnacle Ridge'
		return socket,codename.upper()

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
	distinct_cpus, all_cpus =  CPUscrap()
	distinct_mobos, all_mobos = MOBOscrap()
	distinct_gpus, all_gpus = GPUscrap()
	distinct_rams, all_rams = RAMscrap()
	
	#id, brand, desc, series, gen, socket, codename, unlocked for CPU
	#id,brand,title,chipset,vendor,socket for MOBO
	CPUdistinctinsert = []
	MOBOdistinctinsert = []
	GPUdistinctinsert = []
	RAMdistinctinsert = []
	products = []
	CPUallinsert=[]
	MOBOallinsert=[]
	GPUallinsert=[]
	RAMallinsert=[]
	for cpu in distinct_cpus:
		CPUdistinctinsert.append(tuple((cpu.id,cpu.brand,cpu.series,cpu.gen,cpu.socket,cpu.codename,cpu.unlocked,cpu.image,0)))
		products.append(tuple((cpu.id,cpu.title,'CPU',cpu.image)))
	for mobo in distinct_mobos:
		MOBOdistinctinsert.append(tuple((mobo.id,mobo.brand,mobo.chipset,mobo.vendor,mobo.socket,mobo.image,0)))
		products.append(tuple((mobo.id,mobo.title,'MOBO',mobo.image)))
	for gpu in distinct_gpus:
		GPUdistinctinsert.append(tuple((gpu.id,gpu.model,gpu.brand,gpu.vendor,gpu.image,0)))
		products.append(tuple((gpu.id,gpu.title,'GPU',gpu.image)))
	for ram in distinct_rams:
		RAMdistinctinsert.append(tuple((ram.id,ram.brand,ram.size,ram.rate,ram.speed,ram.image,0)))
		products.append(tuple((ram.id,ram.title,'RAM',ram.image)))
	for gpu in all_gpus:
		GPUallinsert.append(tuple((gpu.id,gpu.price,gpu.link,gpu.seller)))
	for cpu in all_cpus:
		CPUallinsert.append(tuple((cpu.id,cpu.price,cpu.link,cpu.seller)))
	for mobo in all_mobos:
		MOBOallinsert.append(tuple((mobo.id,mobo.price,mobo.link,mobo.seller)))
	for ram in all_rams:
		RAMallinsert.append(tuple((ram.id,ram.price,ram.link,ram.seller)))

	
	try:
		dbconn=mysql.connector.connect(
		host=config.host,
		user=config.user,
		passwd=config.passwd,
		database=config.database
		)
	
		CPUquery="INSERT INTO processor values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		CPUpricesquery="INSERT INTO processor_prices values(%s, %s, %s, %s)"
		MOBOquery="INSERT INTO motherboard values(%s, %s, %s, %s, %s, %s, %s)"
		MOBOpricesquery="INSERT INTO motherboard_prices values(%s, %s, %s, %s)"
		GPUquery="INSERT INTO gpu values(%s, %s, %s, %s, %s, %s)"
		GPUpricesquery="INSERT INTO gpu_prices values(%s, %s, %s, %s)"
		RAMquery = "INSERT INTO ram values(%s, %s, %s, %s, %s,%s, %s)"
		RAMpricesquery="INSERT INTO ram_prices values(%s, %s, %s, %s)"
		PRODUCTSquery="INSERT INTO product values(%s,%s,%s,%s)"
		cursor = dbconn.cursor(prepared=True)
		cursor.execute("set foreign_key_checks = 0")
		cursor.execute("truncate motherboard")
		cursor.execute("truncate motherboard_prices")
		cursor.execute("truncate processor")
		cursor.execute("truncate processor_prices")
		cursor.execute("truncate gpu")
		cursor.execute("truncate gpu_prices")
		cursor.execute("truncate ram")
		cursor.execute("truncate ram_prices")
		cursor.execute("truncate product")
		dbconn.commit()
		cursor.executemany(CPUquery,CPUdistinctinsert)
		cursor.executemany(CPUpricesquery,CPUallinsert)
		cursor.executemany(MOBOquery,MOBOdistinctinsert)
		cursor.executemany(MOBOpricesquery,MOBOallinsert)
		cursor.executemany(GPUquery,GPUdistinctinsert)
		cursor.executemany(GPUpricesquery,GPUallinsert)
		cursor.executemany(RAMquery,RAMdistinctinsert)
		cursor.executemany(RAMpricesquery,RAMallinsert)
		cursor.executemany(PRODUCTSquery,products)
		cursor.execute("update ram set min_price = (select min(price) from ram_prices where ram_prices.id = ram.id)")
		cursor.execute("update processor set min_price = (select min(price) from processor_prices where processor_prices.id = processor.id)")
		cursor.execute("update motherboard set min_price = (select min(price) from motherboard_prices where motherboard_prices.id = motherboard.id)")
		cursor.execute("update gpu set min_price = (select min(price) from gpu_prices where gpu_prices.id = gpu.id)")
		

		cursor.execute("set foreign_key_checks = 1")
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

