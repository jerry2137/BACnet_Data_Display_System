import os
import sys
from bs4 import BeautifulSoup as bs
import pandas as pd
import math

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))

def append_table(soup, building):
    df_file = pd.read_csv(cwd + '/source/data/' + building + '.csv')
    df_name = pd.read_csv(cwd + '/source/raw/rank.csv', index_col='Page')

    number = 0
    for name, df in list(df_file.groupby('Page')):
        for i in range(math.ceil(len(df)/5)):
            number += 1
            div_full = soup.new_tag('div', **{'class':'full'})
            table_df = df[i*5:i*5+5][['Shown Name', 'Value', 'Unit']]

            table_df = pd.concat([table_df, pd.DataFrame([['\\'] * table_df.shape[1]] * (5 - len(table_df)), columns=table_df.columns)])

            html_df = table_df.to_html(index=False, header=False, table_id='table_' + str(number))
            html_df = html_df.replace('border="1" ', '').replace('<td>\\', '<td id="hide">\\<br />\\').replace('\\n', '<br />')

            table = bs(html_df, 'html.parser')
            chinese, english = df_name['Name'][name].split('\n')
            thead = bs('<thead><tr><th colspan="3">' + chinese + '<br />' + english + '</th></tr></thead>', 'html.parser')
            table.find('tbody').insert_before(thead)

            div_full.append(table)
            soup.find('section', {'id':'tables'}).append(div_full)


def to_html(code):
    blocks = pd.read_csv(cwd + '/source/raw/blocks.csv', index_col='Block No.')
    if code not in blocks.index:
        return 'code not found'
    print(blocks['Name'][code])

    with open(cwd + '/templates/template.html', encoding="utf8") as template:
        soup = bs(template, 'html.parser')

    append_table(soup, blocks['Name'][code])
    # append_table(soup, blocks['Name']['B01']) #B00

    chinese_estate, english_estate = blocks['Name']['B00'].split('_', 1)
    estate = bs('<div>' + chinese_estate + '</div><div>' + english_estate + '</div>', 'html.parser')
    soup.find('footer').append(estate)

    chinese_building,  english_building = blocks['Name'][code].split('_', 1)
    building = bs(chinese_building + '<br />' + english_building, 'html.parser')
    soup.find('div', {'id':'building'}).append(building)

    for file in os.listdir(cwd + '/static'):
        if file.endswith('.mp4'):
            video = bs('<video autoplay="" muted="" src="../files/' + file + '"></video>', 'html.parser')
            soup.find('section', {'id':'videos'}).append(video)
        if file.endswith('.jpg'):
            logo = bs('<img id="logo" src="../files/' + file + '" />', 'html.parser')
            soup.find('div', {'id':'system'}).append(logo)
    
    return soup.prettify()

if __name__ == '__main__':
    with open(cwd + '/templates/output.html', 'w', encoding="utf8") as output:
        output.write(to_html('B02'))