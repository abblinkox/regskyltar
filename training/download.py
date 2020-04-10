import requests, time,json, re
from bs4 import BeautifulSoup

# import the necessary packages
from imutils import paths
import argparse
import cv2
import os

urls = []

def scrapeData():
    for page in range(100):
        r = requests.get("https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cg=1020&page=" + str(page+1))
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.find_all("img", {"class": "ListImage__StyledImg-sc-1rp77jc-1 iwClwW"})

        for img in imgs:
            url = img["src"].split("?")[0] + "?type=original"
            urls.append(url)
            print(url)


def download(urls):
    # loop the URLs
    total = 0 
    for url in urls:
        try:
            # try to download the image
            r = requests.get(url, timeout=60)
            # save the image to disk
            p = "downloads/{}.jpg".format(str(total).zfill(8))
            f = open(p, "wb")
            f.write(r.content)
            f.close()
            # update the counter
            print("[INFO] downloaded: {}".format(p))
            total += 1
        # handle if any exceptions are thrown during the download process
        except:
            print("[INFO] error downloading {}...skipping".format(p))
    verify()

def verify():
    for imagePath in paths.list_images("dowloads"):
	# initialize if the image should be deleted or not
        delete = False
        # try to load the image
        try:
            image = cv2.imread(imagePath)
            # if the image is `None` then we could not properly load it
            # from disk, so delete it
            if image is None:
                delete = True
        # if OpenCV cannot load the image then the image is likely
        # corrupt so we should delete it
        except:
            print("Except")
            delete = True
        # check to see if the image should be deleted
        if delete:
            print("[INFO] deleting {}".format(imagePath))
            os.remove(imagePath)


scrapeData()
download(urls)