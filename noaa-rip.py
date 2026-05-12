import requests as req
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote



def get_filename_from_url(url):
	# Parse the URL to get the path
	parsed_url = urlparse(url)
	path = parsed_url.path

	# Extract the last part of the path (the filename)
	# unquote handles percent-encoded characters (e.g., %20 for space)
	filename = unquote(os.path.basename(path))
	return filename

if not os.path.exists("norm"):
    os.makedirs("norm")

if not os.path.exists("mini"):
    os.makedirs("mini")

rawdata = req.get("https://www.ndbc.noaa.gov/to_station.shtml")

webdata = rawdata.text

slSoup = BeautifulSoup(webdata, features="html.parser")

stationList = slSoup.find_all("div", {"class": "station-list"})

for station_div in stationList:
	all_links = station_div.find_all("a")
	for link in all_links:
		station_id = link.text.strip()

		station_path = link['href'].strip()
		rawdata = req.get("https://www.ndbc.noaa.gov/" + station_path)

		soup = BeautifulSoup(rawdata.text, features="html.parser")
		imgelement = soup.find("img", {"class": "station-photo"})

		if imgelement:
			img = imgelement.get("src")

			if img.startswith('/'):
				img_url = "https://www.ndbc.noaa.gov" + img
			else:
				img_url = "https://www.ndbc.noaa.gov/" + img

			mini_filename = get_filename_from_url(img_url).replace('_mini.jpg.jpg', '_mini.jpg')
			mini_path = os.path.join("mini", mini_filename)
			if not os.path.exists(mini_path):
				print("[+] Downloading " + img_url)
				imgfile = req.get(img_url, stream=True)

				content_type = imgfile.headers.get('Content-Type', '')

				if imgfile.status_code == 200 and 'image' in content_type:
					filename = f"{get_filename_from_url(img_url).replace('_mini.jpg.jpg', '_mini.jpg')}"
					with open("mini/" + filename, "wb") as file:
						for chunk in imgfile.iter_content(chunk_size=8192):
        						if chunk:
            							file.write(chunk)
			img_url_norm = img_url.replace("_mini.jpg", ".jpg")

			norm_filename = get_filename_from_url(img_url_norm)
			norm_path = os.path.join("norm", norm_filename)
			if not os.path.exists(norm_path):
				print("[+] Downloading " + img_url_norm)
				imgfile = req.get(img_url_norm, stream=True)

				content_type = imgfile.headers.get('Content-Type', '')

				if imgfile.status_code == 200 and 'image' in content_type:
					filename = f"{get_filename_from_url(img_url_norm)}"
					with open("norm/" + filename, "wb") as file:
						for chunk in imgfile.iter_content(chunk_size=8192):
        						if chunk:
            							file.write(chunk)
