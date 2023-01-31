from operator import le
from pickle import TRUE
from ssl import OP_NO_RENEGOTIATION
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import re

while True:
    
    interval = 50
    
    fname, fname_new, cls = ([] for i in range(3))

    fname = ['templates\index_b2.html', 'templates\index_b3.html', 'templates\index_b4.html', 'templates\index_b5.html', 'templates\index_b6.html', 'templates\index_b7.html', 'templates\index_b8.html', 'templates\index_b9.html'] 
    fname_new = ['templates\index_b2_new.html', 'templates\index_b3_new.html', 'templates\index_b4_new.html', 'templates\index_b5_new.html', 'templates\index_b6_new.html', 'templates\index_b7_new.html', 'templates\index_b8_new.html', 'templates\index_b9_new.html'] 

    # Accessing DDC data
    base_data = os.path.dirname(os.path.abspath(__file__))
    file_data = open(os.path.join(base_data, 'source\data.csv'))
    data = pd.read_csv(file_data)
    
    # Rewriting HTML file
    for i in range(len(fname)):
        base_html = os.path.dirname(os.path.abspath(__file__))
        file_html = open(os.path.join(base_html, fname[i]), encoding="utf8")   
        soup = bs(file_html, 'html.parser')
        o_dir = os.path.join(base_html, fname_new[i])

        # Finding & Updating Specific Values
        for j in range(len(data['Object Name'])):
            if(soup.find('div', {'id':data['Object Name'][j]})):
                old_text = (soup.find('div', {'id':data['Object Name'][j]}))
                old_text.find(text=re.compile(str(old_text.string))).replace_with(str(data['Value'][j]))

        with open(o_dir, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))
            
        old_text.clear()
   
    time.sleep(interval)