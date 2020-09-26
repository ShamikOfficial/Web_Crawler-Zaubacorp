from bs4 import BeautifulSoup as BS
import requests, json
import pandas as pd
from common import *

#Parser using an User Agent
def parser(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    page=requests.get(url,headers=agent)      #requesting page using an agent
    soup = BS(page.text, 'html.parser')
    return soup

#Initialize scrapping by getting required infi from config json file to extract data
def crawler():
    try:
        with open("config.json") as jdata:          #reading json file
            data = json.load(jdata)                 #calling json objects
            search_pg=data[0]["html"]               #Search link retrieved from config.json
            #outf=data[0]["Outfile_name"]           #Sample data for dev
            url=user_choice(search_pg)              #get user's required link to scrap
            groupedlist1=Extract_Zauba_indi(url)                     #final individual company data packed into list of lists
            #uncomment the below line to get excel output
            store_excel(str(url.split("/")[-2]),groupedlist1)       #storing individual company data in excel
            #uncomment the below line to get json1 output
            store_json(str(url.split("/")[-2]),groupedlist1)       #storing individual company data in excel
            print("Scrapping completed Succesfully!!!")
    except Exception as E:
        print('Oops scrapping unsuccessful\nError: ',E)
#Command Line Choices Display
def user_choice(search_pg):
    print("Welcome to Speed Crawler")
    mode=0
    url=""
    search_key=""
    temp=""
    try:
        mode=int(input("Please enter required mode number from options below:\n1 - Download Single Data by CIN number \n2 - Download Single Data by Top Search\n3 - Download Single Data by Exact Zaubacorp Link\n\nChoice: "))
        if (mode==2):
            search_key=str(input("Enter Search Keyword: "))
            url=zauba_top_search(search_pg,search_key)
            return url
        if (mode==1):
            search_key=(input("Enter CIN number: "))
            url=str(search_pg+search_key)
            print(url)
            temp = requests.get(url)
            url=temp.url
            return url
        if (mode==3):
            url=str(input("Enter exact Zaubacorp link: "))
            return url
    except:
        print("Exiting program as no suitable response recieved")
        exit()

#Returns the Best Search Link
def zauba_top_search(search_pg,search_key):
    #search_key="sun" #sample search for devs
    top_link=""
    soup2=""
    company_link=str(search_pg+search_key)
    try:
        soup2=parser(company_link)
        search_data=(soup2.find("div",{"class":"col-xs-12"}))
        top_link =search_data.find_all("table")[0].find("a").get("href")    #GET FIRST SEARCH LINK
        print("\nScrapping initiated . . .")
        return str(top_link)
    except:
        print("No search result found for "+search_key)
        exit()

#Pack the details of a specific company in a list.
def Extract_Zauba_indi(url):
    try:
        soup=parser(url)    #calling nested function
        details=(soup.find_all("div",{"class":"col-lg-12 col-md-12 col-sm-12 col-xs-12"}))
        #print(details)
        i=0
        #Scraping all tabulated Company Details from Zauba Corp
        groupedlist1=[]
        for i in range(20):
            list1=[]
            list2=[]
            field1=[]
            field2=[]
            try:
                field1 = details[i].find_all("table")[0].find_all("tr")     #Table Contents
                field2 = details[i].find_all("h4")[0].text.strip()          #Name of dataframe
            except:
                continue
            for element in field1:
                sub_data = []
                for sub_element in element:
                    try:
                        sub_data.append(sub_element.text.strip())
                    except:
                        continue
                list1.append(sub_data)
            list2.append(field2[:29])   #name of table scrapped to save as sheet name - less than 32 characters
            list2.append(list1)         #fial data without table name
            groupedlist1.append(list2)  #final list of data scraped with table name
            #print(field2,"\n",list1)
        print("Succesfully Extracted Data")
        return groupedlist1
    except:
        print("Oops, No matching Results, exiting Scrapper")
        exit()



if __name__ == '__main__':
    crawler()
