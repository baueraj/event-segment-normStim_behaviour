def add_trial_IDs(df, noExPerTRID):
    """
    adds a column "trialID" based on subject no. (mod 11)
    all hard-coded specific to this experiment
    
    Parameters
    ----------
    df : pandas data frame
        contains the data
    noExPerTRID: list
        contains no. of examples per condition (see init_esn3.py)

    Returns
    -------
    df_wIDs: pandas data frame
        contains the data plus new column of trial IDs

    Notes
    -----
    NA
    """

    import numpy as np
    #np.set_printoptions(threshold = np.nan)
    import pandas as pd
    import init_esn3 #contains variables like dFilePath, tcs

    mod_trialIDs = {'0':  ((1, 2), (1, 1))            
                }
    
    mod_subjIDs = df['subject'].values % 1
                    
    trialIDs = np.empty(len(mod_subjIDs)) * np.nan
    exemplarIDs = np.empty(len(mod_subjIDs)) * np.nan
    itemIDs = np.empty(len(mod_subjIDs)) * np.nan
    
    #mods = list(mod_trialIDs.keys())           
    
    for key in mod_trialIDs.keys():
        ind_key = np.where(mod_subjIDs == int(key))[0]
        trIDs_key = mod_trialIDs[key][0][:]
        exIDs_key = mod_trialIDs[key][1][:]
        
        for idx, i in enumerate(ind_key):
            tc_i = df.iloc[i, 3]
            if tc_i == init_esn3.tcs[trIDs_key[0] - 1]:
                trialIDs[i] = trIDs_key[0]
                exemplarIDs[i] = exIDs_key[0]
                itemIDs[i] = sum(noExPerTRID[0:(trIDs_key[0] - 1)]) + exIDs_key[0]
            elif tc_i == init_esn3.tcs[trIDs_key[1] - 1]:
                trialIDs[i] = trIDs_key[1]
                exemplarIDs[i] = exIDs_key[1]
                itemIDs[i] = sum(noExPerTRID[0:(trIDs_key[1] - 1)]) + exIDs_key[1]
    
    d = {'trialID': trialIDs.astype(int), 'exemplarID': exemplarIDs.astype(int), 'itemID': itemIDs.astype(int)}
    df_add = pd.DataFrame(data=d, index=df.index)
    df_wIDs = pd.concat([df, df_add], axis=1)
    
    return df_wIDs



def rt_threshold_data(df, hthreshold, col_name):
    """
    drops rows in df if latency falls above high threshold
    
    Parameters
    ----------
    df : pandas data frame
        contains the data
    hthreshold : int
        specifies high RT threshold (ms)
    col_name : string
        specifies df column name to access for thresholding

    Returns
    -------
    df_wThresh: pandas data frame
        contains the data with changes made (stated above)

    Notes
    -----
    NA
    """

    import numpy as np
    #np.set_printoptions(threshold = np.nan)
    import pandas as pd
    import init_esn3 #contains variables like dFilePath, tcs

    np_RTs = df[col_name].values
    hth_ind = np.where(np_RTs > hthreshold)[0]
    #np_correct = df['correct'].values
    df_wThresh = df.copy()
    df_wThresh.drop(df_wThresh.index[hth_ind], inplace=True)

    df_wThresh.reset_index(drop=True, inplace=True)
    
    return df_wThresh


    
def plot_three_lines(df, y_lims, ptitle):
    """
    plot three data sources superimposed on same figure
    
    Parameters
    ----------
    df : pandas data frame
        contains the three columns to be plotted together
    y_lims : dictionary of lists
        contains the [min, max] for each df column to be plotted
    ptitle : string
        plot title

    Returns
    -------
    NA

    Notes
    -----
    NA
    """
    
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    
    #plt.figure()
    fig, ax = plt.subplots()
    ax2, ax3 = ax.twinx(), ax.twinx()
    ax3.spines['right'].set_position(('axes', 1.15))
    ax3.set_frame_on(True)
    ax3.patch.set_visible(False)
    fig.subplots_adjust(right=0.75)
    
    ax.tick_params(axis='y', colors='blue')
    ax3.tick_params(axis='y', colors='red')
    
    ax3.set_xticks(range(len(df.index)))
    ax3.set_xticklabels(df.index, fontsize = 20)
    
    df.iloc[:,0].plot(ax=ax, linewidth=3, style='b-')
    df.iloc[:,1].plot(ax=ax2, linewidth=3, style='k-', secondary_y=True)
    df.iloc[:,2].plot(ax=ax3, linewidth=3, style='r-', title=ptitle)
    
    ax.set_ylim(y_lims[df.columns[0]])
    ax2.right_ax.set_ylim(y_lims[df.columns[1]])
    ax3.set_ylim(y_lims[df.columns[2]])
    
    ax.tick_params(labelsize = 20)
    ax2.right_ax.tick_params(labelsize = 20)
    ax3.tick_params(labelsize = 20)
    
    

def prep_data_wi_ttest(df):
    """
    prepares the data for the within-subjects ttest
    
    Parameters
    ----------
    df : pandas data frame
        contains the data AFTER add_trial_IDs reformatting but BEFORE RT thresholding

    Returns
    -------
    df_prep: pandas data frame
        contains the data reformatted for the ttest to be applied

    Notes
    -----
    NA
    """

    import numpy as np
    #np.set_printoptions(threshold = np.nan)
    import pandas as pd
    import init_esn3 #contains variables like dFilePath, tcs
    
    df_wi = df[(df['trialID'] == 1) | (df['trialID'] == 3)]
    df_wi.reset_index(drop=True, inplace=True)
    df_ac = df[(df['trialID'] == 2) | (df['trialID'] == 4)]
    df_ac.reset_index(drop=True, inplace=True)
    
    #ser_add_corrects = pd.Series(data = df_wi['correct'].values + df_ac['correct'].values)
    
    df_prep = pd.concat([df_wi['subject'], df_wi['latency'], df_ac['latency'], df_wi['correct'], df_ac['correct']],
                        axis=1, keys=['subject', 'wi_latency', 'ac_latency', 'wi_correct', 'ac_correct'])
    
    return df_prep