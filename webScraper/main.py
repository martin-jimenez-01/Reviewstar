import time
import os
import csv
import requests
from bs4 import BeautifulSoup

#set the current page count for the reviews
pageCnt = 0

cnt = 0
with open('cities.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for line in csv_reader:
        city = ','.join(line)
        print(city)
        print(cnt)
        #if an old reviews.csv exists, remove it
        if(os.path.exists(city + "-reviews.csv") and os.path.isfile(city + "-reviews.csv")):
            os.remove(city + "-reviews.csv")
        #loop through each reviews page on yelp
        while(pageCnt != 60) :
            url = "https://www.yelp.com/biz/american-airlines-" + city + "?start=" +   str(pageCnt) + "#reviews"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            #find each review
            reviews = soup.find_all('span', class_='raw__09f24__T4Ezm')
            #set false positive counter
            i = 0
            #open up the reviews.csv file in append mode
            with open(city + "-reviews.csv", mode='a', newline='') as csv_file:
                fieldnames = []
                writer = csv.writer(csv_file)
                for review in reviews:
                    #remove garbage data and when complete write the review to the file
                    if(i == 5):
                        writer.writerow([review.text.strip()])
                        print("Reviews have been successfully scraped and saved to " + city + "-reviews.csv!")
                    else:
                        i = i + 1
            #increase the page count
            pageCnt += 10
            #sleep for one second
            time.sleep(1)
          
    #print out successful review scrape
        pageCnt = 0
        time.sleep(20)
    cnt = cnt + 1