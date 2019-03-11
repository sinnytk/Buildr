import requests
import re
import csv
from bs4 import BeautifulSoup

#creating a class for easy usage of objects

def CPUscrap(link):
	#scraping from czone for now
	CPUs = []
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
			CPUs.append(CPU(pn,pp))
	return CPUs


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

	#function to normalize/parse the content of a CPU product title
	def normalize(self,name, price):
		data = [] 
		name.replace(',','').replace('Processor','').replace('Desktop',''); #removing unrequired tags
		data.append(re.findall(("[0-9]{4}K?"),name)[0]) #getting the CPU by using regex to find 4 consecutive occurences of numbers eg 8000k
		data.append(name) #complete title of the product for descriptive purposes
		data.append(re.findall(("(Intel|AMD)"),name)[0]) #regex to find product brand, amd or intel
		data.append(re.findall(("(Core|Ryzen) (i[0-9]|[0-9])"),name)[0]) #regex to find series e.g Ryzen 5 or Core i7
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


# def scrap(link):	
# 	productnames = []
# 	productprices = []
# 	req = requests.get(link)
# 	soup = BeautifulSoup(req.content, "html.parser")
# 	if(soup.find(id="anLastPageBottom").has_attr('href')):
# 		pages = int(soup.find(id="anLastPageBottom")['href'][-1])
# 	else:
# 		print("1 page only")
# 		pages = 1
# 	print("product \t price")
# 	for page in range(pages):
# 		pagelink = link+"?page="+str(page+1)
# 		req = requests.get(pagelink)
# 		soup = BeautifulSoup(req.content, "html.parser")
# 		for product in range(len(soup.find_all("div",class_="template"))-2):
# 			pn='rptListView_ctl0'+str(product)+'_anProductName'
# 			pp='rptListView_ctl0'+str(product)+'_spnPrice'
# 			productnames.append(soup.find(id=pn).text.strip())
# 			productprices.append(soup.find(id=pp).text.strip())

# 	return productnames, productprices
def writecsv(name, prodnames, prodprices):
	productfile = open(name+"_prices.csv",mode="w")
	productfile = csv.writer(productfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for pn,pp in zip(prodnames,prodprices):
		productfile.writerow([pn.split(",")[0],pp])
	
def main():
	# cpuname,cpuprices = scrap("http://czone.com.pk/processors-pakistan-ppt.85.aspx")
	# moboname,moboprices = scrap("http://czone.com.pk/motherboards-pakistan-ppt.157.aspx")
	# gpuname,gpuprices = scrap("http://czone.com.pk/graphic-cards-pakistan-ppt.154.aspx")
	CPUs = CPUscrap('http://czone.com.pk/processors-pakistan-ppt.85.aspx')
	for CPU in CPUs:
		print(CPU.printDetails())
		print("\n\n")
	# writecsv("CPU",cpuname,cpuprices)
	# writecsv("MOBO",moboname,moboprices)
	# writecsv("GPU",gpuname,gpuprices)

if __name__ == "__main__":
	main()

