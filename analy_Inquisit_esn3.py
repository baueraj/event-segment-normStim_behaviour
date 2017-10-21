import os, sys, pdb
import matplotlib.pyplot as plt
plt.show()
import numpy as np
np.set_printoptions(precision = 2)
import pandas as pd
from scipy import stats
from analy_funs_esn2 import *
from init_esn2 import * #contains variables like dFilePath, tcs

os.chdir(expAnalyPath)

columns_to_retain = ["subject", "blocknum", "trialnum", "trialcode", "response", "correct", "latency"]

#retain only certain columns and rows
df_all = pd.read_excel(dFilePath)
df = df_all[columns_to_retain]
df = df[(df["subject"] >= firstSbjID)]
df = df[(df["trialcode"] == tcs[0]) | (df["trialcode"] == tcs[1]) | (df["trialcode"] == tcs[2]) | (df["trialcode"] == tcs[3])]

#add trial IDs and exemplar IDs columns to df
df = add_trial_IDs(df, noExPerTRID)

'''#NOT APPLICABLE IN ROUND 2: fix error in my Inquisit code -- swap correct and incorrect in trialIDs 3 & 4
np_origCorrect = df['correct'].values
np_trialID = df['trialID'].values
ind_bw_origIncorr = np.logical_and(np.logical_or(np_trialID == 3, np_trialID == 4), np_origCorrect == 0)
ind_bw_origCorr = np.logical_and(np.logical_or(np_trialID == 3, np_trialID == 4), np_origCorrect == 1)
#ind_bw_origIncorr = ((df["trialID"] == 3) | (df["trialID"] == 4)) & ((df["correct"] == 0))
#ind_bw_origCorr = ((df["trialID"] == 3) | (df["trialID"] == 4)) & ((df["correct"] == 1))
np_correct = np.copy(np_origCorrect)
np_correct[ind_bw_origIncorr] = 1
np_correct[ind_bw_origCorr] = 0
df['correct'] = np_correct
'''
  
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

within_ind = list(range(0,1)) + list(range(3,8))
across_ind = list(range(1,3)) + list(range(8,10))
plot_three_lines(df_plot.iloc[within_ind,], y_lims, 'within') #HARD-CODED SLICING OF df_plot
plot_three_lines(df_plot.iloc[across_ind,], y_lims, 'across') #HARD-CODED SLICING OF df_plot