import json
import pandas as pd

def get_data(json_data, file_dir):
    temp_data = json.loads(json_data)

    df = pd.DataFrame()

    for item in temp_data['items']:
        item_name = item['item_basic']['name']
        item_price = str(int(item['item_basic']['price'])/100000) + ' ' + item['item_basic']['currency']
        item = pd.Series([item_name, item_price])
        df = df.append(item, ignore_index=True)
        df.to_csv(file_dir)

    return(df)