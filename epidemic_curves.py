# Doing epidemic curve of all, local and non-local cases infection, 
# years 2007 to 2021
# Code developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob
import datetime

files = glob.glob('./Data/processed/*.csv')
data_total = pd.DataFrame()


for file in files:
    # reading data 
    data_test = pd.read_csv(file, 
                            delimiter = ',',
                            index_col=False,
                            parse_dates = ['DT_SIN_PRI','DT_NOTIFIC'], encoding='cp1252')
    # get the year we are working with in question
    # first column is read differently
    data_test = data_test.drop(columns = ['Unnamed: 0'])
    data_total = data_total.append(data_test)
    
# Doing this for basic data analysis    
data_total['CASO'] = 1

# Separating year and epidemiological week
data_total['SEM_EPI'] = data_total['SEM_PRI'].astype(str).str[4:]
data_total['ANO_EPI'] =  data_total['SEM_PRI'].astype(str).str[:4]

# Uniting them with a -
data_total['DATA_EPI'] =  data_total['ANO_EPI'] + '-' + data_total['SEM_EPI']

# Mean age of infection over time, overall cases, epidemiological week
data_age = data_total.groupby(['DATA_EPI'])['NU_IDADE_N'].mean()
data_age = data_age.reset_index()
std_age = data_total.groupby(['DATA_EPI'])['NU_IDADE_N'].std()
std_age = std_age.fillna(0)
std_age = std_age.reset_index()
data_age = data_age.merge(std_age, how = 'left', on = 'DATA_EPI')
data_age.to_csv('./Data/analyzed/national_avg_age.csv')

# National Epidemic Curve first, no difference between local/non-local cases
national_curve = data_total.groupby(['DATA_EPI'])['CASO'].sum()
national_curve = national_curve.reset_index()
national_curve.to_csv('./Data/analyzed/national_epi_curve.csv')

# Curve for cases where Brazil is not the country of residence
res_curve = data_total[data_total['ID_PAIS'] != 1]
res_curve = res_curve.groupby(['DATA_EPI'])['CASO'].sum()
#res_curve = res_curve.groupby(['ID_PAIS'])['CASO'].sum()
res_curve = res_curve.reset_index()
res_curve.to_csv('./Data/analyzed/res_epi_curve.csv')

# Curve for cases where Brazil is not the country of probable infection
inf_curve = data_total[data_total['COPAISINF'] != 1]
inf_curve = inf_curve[inf_curve['COPAISINF'] != 0]
inf_curve = inf_curve.groupby(['DATA_EPI'])['CASO'].sum()
#inf_curve = inf_curve.groupby(['COPAISINF'])['CASO'].sum()
inf_curve = inf_curve.reset_index()
inf_curve.to_csv('./Data/analyzed/inf_epi_curve.csv')
