import os, sys, pdb, json
import matplotlib.pyplot as plt
plt.show()
import numpy as np
np.set_printoptions(precision = 2)
import pandas as pd
from scipy import stats
from analy_funs_esn3 import *
from init_esn3 import * #contains variables like dFilePath, tcs
import sqlite3 as sql

os.chdir(expAnalyPath)

columns_to_retain = ["subject", "blocknum", "trialnum", "trialcode", "response", "correct", "latency"]

#retain only certain columns and rows; SQULITE3 ====================================================================== SQLITE3
conn = sql.connect('dfs.db')
pd.read_excel(dFilePath).to_sql('df_all', conn, if_exists='replace')
query = ' '.join((
        'SELECT ' + ', '.join((i for i in columns_to_retain)),
        'FROM df_all',
        'WHERE subject >= ' + str(firstSbjID),
        'AND trialcode IN (' + ', '.join(("'" + i + "'" for i in tcs)) + ')'))
df = pd.read_sql_query(query, conn)

#add trial IDs and exemplar IDs columns to df
df = add_trial_IDs(df, noExPerTRID)
  
#reset df index to be continuous vetor starting from 0
df.reset_index(drop=True, inplace=True)
  
#remove data based on RT threshold
df_b4RTThresh = pd.DataFrame.copy(df)
df = rt_threshold_data(df, hthreshold, 'latency')

#"main"-level analysis
#descriptive statistics
df_wi = df[(df['trialID'] == 1) | (df['trialID'] == 3)]
df_ac = df[(df['trialID'] == 2) | (df['trialID'] == 4)]

#accuracy
acc_within = df_wi['correct'].mean()
acc_across = df_ac['correct'].mean()

#RT
RT_within = df_wi[(df_wi['correct'] == 1)]['latency'].mean()
RT_across = df_ac[(df_ac['correct'] == 1)]['latency'].mean()

#prep and save these data
data_save = {'df_all': df,
            'df_wi':  df_wi,
            'df_ac':  df_ac                      
        }
with open('data_esn3.json', 'w') as data_save_obj:
    json.dump(data_save, data_save_obj, cls=JSONEncoder)

#statistical analysis
df_ttests = prep_data_wi_ttest(df_b4RTThresh)
df_ttests = rt_threshold_data(df_ttests, hthreshold, 'wi_latency')
df_ttests = rt_threshold_data(df_ttests, hthreshold, 'ac_latency')

#accuracy
acc_ttest = stats.ttest_rel(df_ttests['wi_correct'], df_ttests['ac_correct'])

#RT
ser_wi_RT_ttests = df_ttests[(df_ttests['wi_correct'] == 1) & (df_ttests['ac_correct'] == 1)]['wi_latency']
ser_ac_RT_ttests = df_ttests[(df_ttests['wi_correct'] == 1) & (df_ttests['ac_correct'] == 1)]['ac_latency']
RT_ttest = stats.ttest_rel(ser_wi_RT_ttests, ser_ac_RT_ttests)

#item analysis
#counts (includes incorrect response trials)
np_unique_items, np_counts_items = np.unique(df['itemID'].values, return_counts = True)
unique_items = list(np_unique_items)

#accuracy
acc_items = [df[(df['itemID'] == i)]['correct'].mean() for i in unique_items]

#RT
RT_items = [df[(df['itemID'] == i) & (df['correct'] == 1)]['latency'].mean() for i in unique_items]

#plot item analysis results by condition (within- and across-boundary
d = {'acc_items': acc_items, 'RT_items': RT_items, 'counts_items': np_counts_items}
df_plot = pd.DataFrame(data=d, index=items_labels)
y_lims = {'acc_items': [min(acc_items), max(acc_items)],
          'RT_items': [min(RT_items), max(RT_items)],
          'counts_items': [np_counts_items.min(), np_counts_items.max()]
        }

within_ind = list(range(0,1))
across_ind = list(range(1,2))
plot_three_lines(df_plot.iloc[within_ind,], y_lims, 'within') #HARD-CODED SLICING OF df_plot
plot_three_lines(df_plot.iloc[across_ind,], y_lims, 'across') #HARD-CODED SLICING OF df_plot