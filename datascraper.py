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
	else:
		pages = 1
	for page in range(pages):
		pagelink = link+"?page="+str(page+1)
		req = requests.get(pagelink)
		soup = BeautifulSoup(req.content, "html.parser")
		for product in range(len(soup.find_all("div",class_="template"))-2):
			pn='rptListView_ctl0'+str(product)+'_anProductName'
			pn = soup.find(id=pn).text.strip()
			pp='rptListView_ctl0'+str(product)+'_spnPrice'
			pp = soup.find(id=pp).text.strip()
			products.append(CPU(pn,pp))
	return products
def PAKDUKAAN(type,link):
	products = []
	req = requests.get(link)
	soup = BeautifulSoup(req.content, 'html.parser')
	pages = len(soup.find_all('ol')[0].find_all('li'))-1
	for page in range(pages):
		pagelink = link+'?'+str(page+1)
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
		

def CPUscrap():
	links = ['http://czone.com.pk/processors-pakistan-ppt.85.aspx','https://www.pakdukaan.com/pc-hardware-accessories/processors','https://www.galaxy.pk/pc-addons/processor/intel.html','https://www.galaxy.pk/pc-addons/processor/amd.html']
	CPUs = set()
	CPUs.update(CZONE('CPU',links[0]))
	CPUs.update(PAKDUKAAN('CPU',links[1]))
	CPUs.update(GALAXY('CPU',links[2]))
	return CPUs

#class MOBO:
#	def __init__(self,name, price):
#		data = self.normalize(name, price)
		
class CPU:
	def __init__(self,name, price):
		data = self.normalize(name, price)
		self.CPUid = data[0]
		self.CPUtitle = data[1]
		self.CPUbrand = data[2]
		self.CPUseries = data[3]
		self.CPUgen = data[4]
		self.CPUunlocked = data[5]
		self.CPUprice = data[6]
	def __eq__(self, other):
		return self.CPUid == other.CPUid
		#and (self.CPUtitle == other.CPUtitle) and (self.CPUbrand == other.CPUbrand) and (self.CPUseries == other.CPUseries) and (self.CPUgen == other.CPUgen) and (self.CPUunlocked == other.CPUunlocked)

	def __hash__(self):
		return hash((self.CPUid))

	#function to normalize/parse the content of a CPU product title
	def normalize(self,name, price):
		data = []
		name.replace(',','').replace('Processor','').replace('Desktop','') #removing unrequired tags
		data.append(re.search(("[0-9]{4}(K|k|T|t|P|p|U|u|X|x)?"),name).group(0).upper()) #getting the CPU by using regex to find 4 consecutive occurences of numbers eg 8000k
		data.append(name) #complete title of the product for descriptive purposes
		data.append(re.search(("(Intel|AMD)"),name).group(0)) #regex to find product brand, amd or intel
		data.append(re.search(("(Core|Ryzen)( |-)((i|I)[0-9]|[0-9])"),name).group(0)) #regex to find series e.g Ryzen 5 or Core i7
		if(data[2][0]=='I'): #finding the generation of a cpu from it's ID, intel's first letter of code defines the generation, eg 8000k means 8th gen
			data.append(data[0][0])
		else:
			data.append(data[3][1:][0]) #for AMD it's the letter right after Ryzen, e.g Ryzen 5 means 5th gen
		data[0]=data[2][0]+data[0] #appending company initial in the ID, 'A' or 'I' to descriminate intel and amd
		if(data[2][0]=='A' or data[0][-1:]=='K'): #defining the state of overclockability
			data.append('Yes')
		else:
			data.append('No')
		data.append(int(price.replace(',','')[3:])) #removing Rs. from 'Rs. 20000'
		return data

	def printDetails(self):
		print("CPU ID: %s\nCPUtitle: %s\nCPUbrand: %s\nCPUseries: %s\nCPUgen: %s\nUnlocked: %s\nPrice: %d" %(self.CPUid, self.CPUtitle, self.CPUbrand, self.CPUseries, self.CPUgen, self.CPUunlocked, self.CPUprice))
	
def main():
	CPUs = CPUscrap()
	print(len(CPUs))
	for CPU in CPUs:
		print(CPU.CPUid)

if __name__ == "__main__":
	main()

