import json
import pandas as pd
import numpy as np
from scipy import stats

#concatenate data from different versions of norming experiment
stanPath = '/Users/bauera/Dropbox/UofT/experiments/'

df_wi_esn = pd.read_json(json.load(open(stanPath + 'event-seg_phase2_normStimuli/analysis/data_esn.json'))['df_wi'])
df_wi_esn2 = pd.read_json(json.load(open(stanPath + 'event-seg_phase2_normStimuliV2/analysis/data_esn2.json'))['df_wi'])
df_wi_esn3 = pd.read_json(json.load(open(stanPath + 'event-seg_phase2_normStimuliV3/analysis/data_esn3.json'))['df_wi'])
df_wi = pd.concat([df_wi_esn, df_wi_esn2, df_wi_esn3])
df_wi.reset_index(drop=True, inplace=True)

df_ac_esn = pd.read_json(json.load(open(stanPath + 'event-seg_phase2_normStimuli/analysis/data_esn.json'))['df_ac'])
df_ac_esn2 = pd.read_json(json.load(open(stanPath + 'event-seg_phase2_normStimuliV2/analysis/data_esn2.json'))['df_ac'])
df_ac_esn3 = pd.read_json(json.load(open(stanPath + 'event-seg_phase2_normStimuliV3/analysis/data_esn3.json'))['df_ac'])
df_ac = pd.concat([df_ac_esn, df_ac_esn2, df_ac_esn3])
df_ac.reset_index(drop=True, inplace=True)

#independent sample ttests and descriptive stats
#accuracy
acc_ttest = stats.ttest_ind(df_wi['correct'], df_ac['correct'])
wi_acc_mean = df_wi['correct'].mean()
ac_acc_mean = df_ac['correct'].mean()

#RT
wi_RT_s = df_wi.loc[df_wi['correct'] == 1, 'latency']
ac_RT_s = df_ac.loc[df_ac['correct'] == 1, 'latency']
RT_ttest = stats.ttest_ind(wi_RT_s, ac_RT_s)
wi_RT_mean = wi_RT_s.mean()
ac_RT_mean = ac_RT_s.mean()