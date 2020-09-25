import json
import pandas as pd
import os

#Check and make output directory 
def makedirs():   
    if not os.path.exists('output'):
        os.mkdir('output')

#function to store individual company data in xlsx format
def store_indi(outf,groupedlist1):
    makedirs()
    writer = pd.ExcelWriter('output'+os.path.sep+outf, engine='xlsxwriter')
    for sheet0,list1 in groupedlist1:
        df1 = pd.DataFrame(data = list1,columns=None)
        df1.to_excel(writer, sheet_name=sheet0,index=False,header=False)

    writer.save()
