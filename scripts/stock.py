import io
import json
import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine


def get_yesterday(date_obj):
    diff_day = datetime.timedelta(1)
    date_obj -= diff_day
    return date_obj

def get_workday(date_obj):
    if date_obj.weekday() + 1 in (1,2,3,4,5):
        return date_obj
    else:
        date_obj = get_yesterday(date_obj)
        return get_workday(date_obj)

def write_to_table(df, table_name, if_exists='append'):
    db_engine = create_engine('postgresql+psycopg2://postgres:123456@193.123.248.180:5432/ork')# 初始化引擎
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists)
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = "COPY {} FROM STDIN HEADER DELIMITER '|' CSV".format(table_name)
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()

def get_top_list(date_obj):
    df = raw_top_list(date_obj)
    write_to_table(df, 'stock', if_exists='append')
    return df

def raw_top_list(date_str):
    LHB_URL = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate={startDate},endDate={endDate},gpfw=0,js=vardata_tab_1.html'.format(startDate=date_str, endDate=date_str)
    req = requests.get(url=LHB_URL)
    resp_text = req.text
    resp_json = json.loads(resp_text.replace('vardata_tab_1=', ''))
    resp_data = resp_json.get('data', [])
    df = pd.DataFrame(resp_data, columns=['SCode', 'SName', 'Chgradio', 'ZeMoney', 'Bmoney', 'Smoney', 'Ctypedes', 'Turnover'])
    df.columns = ['code', 'name', 'pchange', 'amount', 'buy', 'sell', 'reason', 'Turnover']
    df = df.fillna(0)
    df = df.replace('', 0)
    df['id'] = range(len(df))
    df['buy'] = df['buy'].astype(float)
    df['sell'] = df['sell'].astype(float)
    df['amount'] = df['amount'].astype(float)
    df['Turnover'] = df['Turnover'].astype(float)
    df['bratio'] = df['buy'] / df['Turnover']
    df['sratio'] = df['sell'] /df['Turnover']
    df['bratio'] = df['bratio'].map(lambda x: '%.2f' % x)
    df['sratio'] = df['sratio'].map(lambda x: '%.2f' % x)
    df['date'] = date_str
    for col in ['amount', 'buy', 'sell']:
        df[col] = df[col].astype(float)
        df[col] = df[col] / 10000
        df[col] = df[col].map(lambda x: '%.2f' % x)
    df = df.drop('Turnover', axis=1)
    return df

today = datetime.date.today()
diff_day = datetime.timedelta(1)
dest_day = today - 0 * diff_day
dest_day_str = dest_day.isoformat()
get_top_list(dest_day_str)
print("Get <{today}> stock data successfully!".format(today=dest_day_str))
