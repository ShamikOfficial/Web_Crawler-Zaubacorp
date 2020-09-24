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
        company_name="BYJU-S-K3-EDUCATION-PRIVATE-LIMITED"
        company_cin="U80900KA2018PTC115288"
        start_pg=data[0]["start_page"]
        stop_pg=data[0]["stop_page"]
        outf=data[0]["Outfile_name"]
        url=str(html+company_name+"/"+company_cin)
        all_list=Extract_Zauba_indi(url)
        #print(all_list)

#Pack the details of a specific company in a list.
def Extract_Zauba_indi(url):
    soup=parser(url)    #calling nested function
    #details=(soup.find_all("div",{"class":"container information"}))
    details=(soup.find_all("div",{"class":"col-lg-12 col-md-12 col-sm-12 col-xs-12"}))
    #print(details)
    i=0
    #Scraping all tabulated Company Details from Zauba Corp
    groupedlist1=[]
    for i in range(20):
        list1=[]
        field1=[]
        field2=[]
        try:
            field1 = details[i].find_all("table")[0].find_all("tr")
            field2 = details[i].find_all("h4")[0].text.strip()  #Name of dataframe
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
        print(field2,"\n")
        print(dataFrame)
    return groupedlist1

if __name__ == '__main__':
    crawler()
