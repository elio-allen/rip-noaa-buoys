import requests as req
from bs4 import BeautifulSoup

rawdata = req.get("https://www.ndbc.noaa.gov/to_station.shtml")

webdata = rawdata.text

slSoup = BeautifulSoup(webdata, features="html.parser")

stationList = slSoup.find_all("div", {"class": "station-list"})

for station in stationList:
	link = station.find("a")
	if not link: continue
	rawdata = req.get("https://www.ndbc.noaa.gov/" + link['href'].strip())
	webdata = rawdata.text

	soup = BeautifulSoup(webdata)
	imgelement = soup.find("img", {"class": "station-photo"})

	if imgelement:
		img = imgelement.get("src")
		imgfile = req.get("https://www.ndbc.noaa.gov/" + img, stream=True)
		filename = img.split("/")[-1]
		with open("out/" + filename, "wb") as file:
			for chunk in imgfile.iter_content(chunk_size=8192):
        			if chunk:
            				file.write(chunk)
