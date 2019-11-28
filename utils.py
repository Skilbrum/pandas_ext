import numpy as np
import pandas as pd
import datetime

def excel_date(date):
    '''
    Converting date to Excel date or from Excel date
    
    Parameters
    ----------
    date : float, int OR str, datetime.datetime, pd.Timestamp
    Excel date as float/int OR date recognized by pandas. 
    
    Returns
    ----------
    date : float, int OR pd.Timestamp
    Excel date as float/int or date as pd.Timestamp.
    '''
    
    #unlike python, 29.02.1900 exists in excel
    #since 01.03.2019 pandas and excel calendar has equal dates
    cons_date = pd.Timestamp(year=1900, month=3, day=1)
    excel_cons_date = 61
    
    if isinstance(date, (str, datetime.datetime, pd.Timestamp)):
        return (pd.to_datetime(date) - cons_date).days + excel_cons_date
    
    elif isinstance(date, (np.int, np.float)):
        return cons_date + pd.Timedelta(days=date - excel_cons_date)
        
    else:
        raise TypeError('expected str, datetime, float, int, got ', type(date))

def time_derivative(series, time_unit=pd.Timedelta('1s')):
    '''
    Calculate time derivative from right for each point in series. Ignores NaN.
    
    Parameters
    ---------
    series: pd.Series with numeric data with pd.DatetimeIndex
    time_unit: pd.Timedelta
    
    Returns
    ---------
    dsdt : pd.Series
    '''
    
    ds=series.dropna().diff()
    dt=ds.index.to_series().diff()
    dsdt=ds/(dt/time_unit)
    return dsdt

def isnumber(a):
    '''Check if string can be converted fo float'''
    try:
        float(a)
        return True
    except:
        return False
    
def convert_cyr_month(series):
    '''Convert cyrillic name of month in series to month number (i.e. 01, 02, ..., 12)
    Parameters
    ----------
    series: pd.Series of str
    
    Returns
    ----------
    series: pd.Series
    '''
    series=series.copy()
    
    repl_dict={
    'янв\\w*' : '01',    
    'фев\\w*' : '02',    
    'мар\\w*' : '03',
    'апр\\w*' : '04',
    'май\\w*' : '05',
    'июн\\w*' : '06',
    'июл\\w*' : '07',
    'авг\\w*' : '08',
    'сен\\w*' : '09',
    'окт\\w*' : '10',
    'ноя\\w*' : '11',
    'дек\\w*' : '12'
    }
    
    for k, v in repl_dict.items():
        series=series.str.replace(k, v)
    
    return series

def read_all_sheets(add_sheet_name=True, **kwargs):
    '''Read all sheets from Excel file
    Parameters
    ----------
    add_sheet_name: bool
    Add to dataframe column with sheet name for each sheet
    pd.ExcelFile **kwargs
    
    Returns
    ----------
    sheets: list of pd.DataFrame
    '''
    book=pd.ExcelFile(**kwargs)
    
    sheets=[]
    for sh in book.sheet_names:
        sheet=book.parse(sh)
        sheet['sheet_name']=sh
        sheets.append(sheet)

    return sheets

def timeseries_info(df):
    
    '''Timeseries start, end and frequency.
    
    Parameters
    ----------
    df: pd.DataFrame or pd.Series with pd.DatetimeIndex
    
    Returns
    ----------
    start: pd.Timestamp
    end: pd.Timestamp
    freq: pd.Series
    '''
    
    start = df.index.min()
    end = df.index.max()
    freq = df.index.to_series().diff().value_counts()
    return start, end, freq

def bool_report(series):
    '''Returns groups of indices for bool series provided from dataframe tests.
    Parameters
    ----------
    series: pd.Series of bool
    
    Returns
    ----------
    report: dict
    '''
    return series.groupby(series).groups
