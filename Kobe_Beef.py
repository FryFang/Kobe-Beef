# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 23:15:42 2020

@author: fryfa
"""
import requests
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup



def get_data(page, year, form):
    for i in range(page+1):
        kobe = "http://www.kobe-niku.jp/en/contents/exported/index.php?y=" + \
                str(year)+"&page="+str(i)
        data = requests.get(kobe)
        soup = BeautifulSoup(data.text, 'html.parser')
    
        for col in range(1,8):
            for ele in soup.find_all('td', class_='td'+str(col)):
                form[col-1].append(ele.text)
    return 1

def gen_df(form):
    df=DataFrame(form)
    df.index = pd.Index(['Export Date', 'Individual ID', 'Country', \
                                  'Weight', 'Producer', 'Exporter', 'Importer'])
    df = df.transpose()
    return df

def get_tot_weight(df):
    df_weight = df.query('Country == "USA"')
    df_weight.reset_index()
    tot=0
    for i in range(len(df_weight.index)):
        tot+= float(df_weight.iloc[i,3][:-2])
    print('Total exported to USA: {:.1f} kg'.format(tot))
    return 1

def main():
    form = [[],[],[],[],[],[],[]]
    page = 7
    year = 2020
    get_data(page, year, form)
    
    df = gen_df(form)
    get_tot_weight(df)
    
    df.to_csv(str(year)+'_Kobe_Exported.csv', index=False, encoding='utf-8-sig')
    
if __name__== "__main__" :
    main()