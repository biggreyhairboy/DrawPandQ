# todo: sqlalchemy core or ORM fro query data more easier
from sqlalchemy import create_engine
import pandas as pd

import pandas as pd

def getaDayTicksFromSQLServer(filemode):
    if filemode == "dbmode":
        sourcedb = "GTA_MFL1_TAQ_201612_new"
        enginestr = "mssql+pyodbc://sa:223223@192.168.93.123:1433/" + sourcedb + "?driver=ODBC+Driver+11+for+SQL+Server"
        gtaengine = create_engine(enginestr)
        # conn = gtaengine.connect()
        myQuery = "select * FROM MFL1_TAQ_RB1710_201612 where TRADINGDATE = '20161201';"
        df = pd.read_sql(myQuery, gtaengine)
        df.to_csv("rb1710_201612.csv")
    elif filemode == "csvmode":
        df = pd.read_csv("rb1710_201612.csv")
    return df

def cleanTicks(dayticks):
    # print(dayticks['HIGHPX'])
    dayticks[['TDATETIME', 'LOCALTIME']] = dayticks[['TDATETIME', 'LOCALTIME']].apply(pd.to_datetime)
    dayticks['realtradingdate'] = [d.date() for d in dayticks['TDATETIME']]
    dayticks['realtradingtime'] = [d.time() for d in dayticks['TDATETIME']]
    # dayticks['realtradingtime'] = dayticks['realtradingtime'].apply(pd.to_datetime)
    print(dayticks.dtypes)
    # and dayticks.realtradingtime < time(20, 58, 0)

    nightticks = dayticks.set_index('TDATETIME').between_time('20:54:59', '23:00:01').reset_index()
    morningticks = dayticks.set_index('TDATETIME').between_time('8:58:59', '23:00:01').reset_index()
    afternoonticks = dayticks.set_index('TDATETIME').between_time('13:29:59', '15:00:01').reset_index()
    frames = [nightticks, morningticks, afternoonticks]
    cleanticks = pd.concat(frames)
    return cleanticks
