from bs4 import BeautifulSoup as BS
import requests, json
import pandas as pd

#Parser using an User Agent
def parser(url):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    page=requests.get(url,headers=agent)      #requesting page using an agent
    soup = BS(page.text, 'html.parser')
    return soup

#Initialize scrapping by getting required infi from config json file to extract data
def crawler():
    with open("config.json") as jdata:            #reading json file
        data = json.load(jdata)

        #calling json objects
        html=data[0]["html"]
        start_pg=data[0]["start_page"]
        stop_pg=data[0]["stop_page"]
        outf=data[0]["Outfile_name"]
        url=(html)
        all_list=Extract(url)
        print(all_list)

#Pack the details of a specific company in a list.
def Extract_Zauba_indi(url):
    soup=parser(url)    #calling nested function
    details=(soup.find_all("div",{"class":"container information"}))
    #print(details)
    i=0
    #Scraping all tabulated Company Details from Zauba Corp
    groupedlist1=[]
    for i in range(20):
        list1=[]
        field1=[]
        try:
            field1 = details[0].find_all("table")[i].find_all("tr")
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
        groupedlist1.append(list1)
        dataFrame = pd.DataFrame(data = list1,columns=None) #create dataframe to export to csv
        print(dataFrame)
    return groupedlist1

if __name__ == '__main__':
    crawler()
