from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

dataset_new=pd.read_csv("csr_full.txt",delimiter="\t", header=None, names=["company links"])#adds column name in the dataframe
for ind, row in dataset_new.iterrows():
    newlink = (row["company links"]) 
    print (newlink)