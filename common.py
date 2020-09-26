import json
import pandas as pd
import os

#Check and make output directory
def makedirs(outf):
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('output'+os.path.sep+'Data-'+outf):
        os.mkdir('output'+os.path.sep+'Data-'+outf)
#function to store individual company data in xlsx format
def store_excel(outf,groupedlist1):
    makedirs(outf)
    try:
        writer = pd.ExcelWriter('output'+os.path.sep+'Data-'+outf+os.path.sep+outf+'.xlsx', engine='xlsxwriter')
        for sheet0,list1 in groupedlist1:
            df1 = pd.DataFrame(data = list1,columns=None)
            df1.to_excel(writer, sheet_name=sheet0,index=False,header=False)
        print("Succesfully saved excel data in Output Folder")
    except:
        print("Some error occured in Saving File")

    writer.save()

#function to store individual company data in json format
def store_json(outf,groupedlist1):
    makedirs(outf)
    try:
        with open('output'+os.path.sep+'Data-'+outf+os.path.sep+outf+'.json','w') as f:
            f.write(json.dumps(groupedlist1))
        print("Succesfully saved json data in Output Folder")
    except:
        print("Some error occured in Saving File")
    