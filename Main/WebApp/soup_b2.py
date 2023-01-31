from operator import le
from pickle import TRUE
from ssl import OP_NO_RENEGOTIATION
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import re

while True:
    
    interval = 9000
    
    cls = ([] for i in range(1))

    base_data = os.path.dirname(os.path.abspath(__file__))    
    file_data = open(os.path.join(base_data, 'source\data.csv'))
    data = pd.read_csv(file_data)
    
    base_html = os.path.dirname(os.path.abspath(__file__))
    file_html = open(os.path.join(base_html, 'templates\index_b2.html'), encoding="utf8")     
    soup = bs(file_html, 'html.parser')
    o_dir = os.path.join(base_html, 'templates\index_b2_new.html') 

    for i in range(len(data['Object Name'])):
        if(soup.find('div', {'id':data['Object Name'][i]})): 
            old_text = soup.find('div', {'id':data['Object Name'][i]})
            old_text.find(text=re.compile(str(old_text.string))).replace_with(str(data['Value'][i]))
            print(old_text)
    
    
    
    with open(o_dir, "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))
    
    time.sleep(interval)