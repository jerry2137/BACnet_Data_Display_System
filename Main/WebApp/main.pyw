import sys
import BAC0
import pandas as pd
import os
# import time

# bacnet = BAC0.connect(ip='192.168.1.51/24')
# interval = 5

# # Main Function #
# def connect_device():
#     # File for raw data #
#     cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
#     raw = pd.read_csv(cwd + '/source/raw/raw.csv')
#     points = pd.read_csv(cwd + '/source/raw/points.csv', index_col='BACnet Object Name')
#     blocks = pd.read_csv(cwd + '/source/raw/blocks.csv', index_col='Block No.')
#     raw.columns = raw.columns.str.replace(' ', '_')

#     #get all devices
#     bacnet.whois()
#     devices = pd.DataFrame(bacnet.devices)

#     while True:
#         # Reading properties from device #
#         df = pd.DataFrame(columns=['Shown Name', 'Value', 'Unit', 'Block', 'Page'])
#         df.index.name = 'Object Name'

#         for row in raw.itertuples():
#             for device in devices.itertuples(index=False):
#                 if row.Device_Name == device[0]:
#                     read = str(device[2]) + ' ' + row.BACnet_Object_type + ' ' + str(int(row.BACnet_Object_Instance)) + ' presentValue'
#                     block, point = row.BACnet_Object_Name.split('-', 1)
#                     if point in points.index:
#                         df.loc[row.BACnet_Object_Name] = [
#                             points['Shown Name'][point],
#                             "{:.1f}".format(bacnet.read(read)),
#                             points['Unit'][point],
#                             block,
#                             points['Page'][point],
#                         ]
#                     else:
#                         df.loc[row.BACnet_Object_Name] = ['point not found', "{:.1f}".format(bacnet.read(read)), 'point not found', block, 'point not found']
#                     break

#         print(df, "\n")
#         for code, df_block in df.groupby('Block'):
#             if code in blocks.index:
#                 df_block.loc[:, df_block.columns!='Block'].to_csv(cwd + '/source/data/' + blocks['Name'][code] + '.csv')
#             else:
#                 df_block.loc[:, df_block.columns!='Block'].to_csv(cwd + '/source/data/' + blocks['Name']['B01'] + '.csv')

#         time.sleep(interval)
        

def to_df():
    # File for raw data #
    cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
    raw = pd.read_csv(cwd + '/source/raw/raw.csv')
    points = pd.read_csv(cwd + '/source/raw/points.csv', index_col='BACnet Object Name')
    blocks = pd.read_csv(cwd + '/source/raw/blocks.csv', index_col='Block No.')
    raw.columns = raw.columns.str.replace(' ', '_')

    #get all devices
    bacnet = BAC0.connect(ip='192.168.1.51/24')
    bacnet.whois()
    devices = pd.DataFrame(bacnet.devices)

    # Reading properties from device #
    df = pd.DataFrame(columns=['Shown Name', 'Value', 'Unit', 'Block', 'Page'])
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
        

if __name__ == '__main__':
    # connect_device()
    to_df()