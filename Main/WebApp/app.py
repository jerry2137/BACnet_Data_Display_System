from flask import Flask, send_from_directory
from waitress import serve
import os
import sys
from bs4 import BeautifulSoup as bs
from pandas import DataFrame,  read_csv, concat
import math
import BAC0

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
app = Flask(__name__)

def append_table(soup, building):
    df_file = read_csv(cwd + '/source/data/' + building + '.csv')
    df_name = read_csv(cwd + '/source/raw/rank.csv', index_col='Page')

    number = 0
    for name, df in list(df_file.groupby('Page')):
        for i in range(math.ceil(len(df)/5)):
            number += 1
            div_full = soup.new_tag('div', **{'class':'full'})
            table_df = df[i*5:i*5+5][['Shown Name', 'Value', 'Unit']]

            table_df = concat([table_df, DataFrame([['\\'] * table_df.shape[1]] * (5 - len(table_df)), columns=table_df.columns)])

            html_df = table_df.to_html(index=False, header=False, table_id='table_' + str(number))
            html_df = html_df.replace('border="1" ', '').replace('<td>\\', '<td id="hide">\\<br />\\').replace('\\n', '<br />')

            table = bs(html_df, 'html.parser')
            chinese, english = df_name['Name'][name].split('\n')
            thead = bs('<thead><tr><th colspan="3">' + chinese + '<br />' + english + '</th></tr></thead>', 'html.parser')
            table.find('tbody').insert_before(thead)

            div_full.append(table)
            soup.find('section', {'id':'tables'}).append(div_full)


def to_html(code):
    blocks = read_csv(cwd + '/source/raw/blocks.csv', index_col='Block No.')
    if code not in blocks.index:
        return 'code not found'
    print(blocks['Name'][code])

    with open(cwd + '/templates/template.html', encoding="utf8") as template:
        soup = bs(template, 'html.parser')

    append_table(soup, blocks['Name'][code])
    # append_table(soup, blocks['Name']['B01']) #B00

    for estate_name in blocks['Name']['B00'].split('_'):
        div_footer = soup.new_tag('div')
        div_footer.string = estate_name
        soup.find('footer').append(div_footer)

    chinese_building,  english_building = blocks['Name'][code].split('_')
    soup.find('div', {'id':'building'}).append(chinese_building)
    soup.find('div', {'id':'building'}).append(soup.new_tag('br'))
    soup.find('div', {'id':'building'}).append(english_building)
    return soup.prettify()
    
def to_df():
    # File for raw data #
    cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
    raw = read_csv(cwd + '/source/raw/raw.csv')
    points = read_csv(cwd + '/source/raw/points.csv', index_col='BACnet Object Name')
    blocks = read_csv(cwd + '/source/raw/blocks.csv', index_col='Block No.')
    raw.columns = raw.columns.str.replace(' ', '_')

    #get all devices
    bacnet = BAC0.connect(ip='192.168.1.51/24')
    bacnet.whois()
    devices = DataFrame(bacnet.devices)

    # Reading properties from device #
    df = DataFrame(columns=['Shown Name', 'Value', 'Unit', 'Block', 'Page'])
    df.index.name = 'Object Name'

    for row in raw.itertuples():
        for device in devices.itertuples(index=False):
            if row.Device_Name == device[0]:
                read = str(device[2]) + ' ' + row.BACnet_Object_type + ' ' + str(int(row.BACnet_Object_Instance)) + ' presentValue'
                block, point = row.BACnet_Object_Name.split('-', 1)
                if point in points.index:
                    df.loc[row.BACnet_Object_Name] = [
                        points['Shown Name'][point],
                        "{:.1f}".format(bacnet.read(read)),
                        points['Unit'][point],
                        block,
                        points['Page'][point],
                    ]
                else:
                    df.loc[row.BACnet_Object_Name] = ['point not found', "{:.1f}".format(bacnet.read(read)), 'point not found', block, 'point not found']
                break

    print(df, "\n")
    for code, df_block in df.groupby('Block'):
        if code in blocks.index:
            df_block.loc[:, df_block.columns!='Block'].to_csv(cwd + '/source/data/' + blocks['Name'][code] + '.csv')
        else:
            df_block.loc[:, df_block.columns!='Block'].to_csv(cwd + '/source/data/' + blocks['Name']['B01'] + '.csv')

    bacnet.disconnect()

@app.route('/buildings/files/<string:filename>/')
def get_css(filename):
    return send_from_directory('static', filename)

@app.route('/buildings/<string:code>/')
def get_html(code):
    to_df()
    return to_html(code)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    serve(app, host='0.0.0.0', port=5000)