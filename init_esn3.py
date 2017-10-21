import os, sys, json
#import numpy as np
#np.set_printoptions(threshold = np.nan)
#import pandas as pd
#sys.path.append(os.getcwd())
#from analy_funs_esn import *

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)

expAnalyPath = '/Users/bauera/Dropbox/UofT/experiments/event-seg_phase2_normStimuliV3/analysis'
dFilePath = expAnalyPath + '/../data/main_objmemnorm_round3_raw_17_07_10.xlsx'
firstSbjID = 18
hthreshold = 3000 #ms
noExPerTRID= [1, 1] #busyworld within, busyworld across
items_labels = ['bw1', 'ba1']
tc3 = "show_busyworld_within_pictures"
tc4 = "show_busyworld_across_pictures"
tcs = [tc3, tc4]