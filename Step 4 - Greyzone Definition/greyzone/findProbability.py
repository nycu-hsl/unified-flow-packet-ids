import pandas as pd
import numpy as np
import sys

# CSV_FILE_NAME = "data_for_greyzone_threshold.csv"
PERCENTILE_ITERATION = 1000
CONFIDENCE_SAMPLES_PERCENTAGE = 0.005

def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

def start_finding_greyzone_threshold(rawData, save_place):
    # rawData = pd.DataFrame(pd.read_csv(CSV_FILE_NAME), columns=['label', 'detection_results', 'detection_probability'])
    data00Sets = rawData.loc[(rawData['label']==0)&(rawData['detection_results']==0)]
    data10Sets = rawData.loc[(rawData['label']==1)&(rawData['detection_results']==0)]
    data01Sets = rawData.loc[(rawData['label']==0)&(rawData['detection_results']==1)]
    data11Sets = rawData.loc[(rawData['label']==1)&(rawData['detection_results']==1)]

    tdTable = []
    teTable = []
    tdMaxProbability = data10Sets['detection_probability'].dropna().quantile(1)
    teMinProbability = data01Sets['detection_probability'].dropna().quantile(0)

    for x in progressbar(range(0, PERCENTILE_ITERATION+1), "Iteration: ", 60):
        percentile = x/PERCENTILE_ITERATION

        tdProbability = data10Sets['detection_probability'].dropna().quantile(percentile)
        size00Sets = data00Sets.loc[(tdMaxProbability >= data00Sets['detection_probability'])&(data00Sets['detection_probability'] >= tdProbability)].shape[0]
        size10Sets = data10Sets.loc[(tdMaxProbability >= data10Sets['detection_probability'])&(data10Sets['detection_probability'] >= tdProbability)].shape[0]
        tdRatio = size10Sets/size00Sets if size00Sets != 0 else float("inf")
        tdCredibility = (size00Sets != 0) & (size00Sets < data00Sets.shape[0] * CONFIDENCE_SAMPLES_PERCENTAGE)
        tdTable.append([percentile, tdProbability, size00Sets, size10Sets, tdRatio, tdCredibility])
        
        teProbability = data01Sets['detection_probability'].dropna().quantile(percentile)
        size11Sets = data11Sets.loc[(teProbability >= data11Sets['detection_probability'])&(data11Sets['detection_probability'] >= teMinProbability)].shape[0]
        size01Sets = data01Sets.loc[(teProbability >= data01Sets['detection_probability'])&(data01Sets['detection_probability'] >= teMinProbability)].shape[0]
        teRatio = size01Sets/size11Sets if size11Sets != 0 else float("-inf")
        teCredibility = (size11Sets != 0) & (size11Sets > data11Sets.shape[0] * CONFIDENCE_SAMPLES_PERCENTAGE)
        teTable.append([percentile, teProbability, size11Sets, size01Sets, teRatio, teCredibility])

    tdDf = pd.DataFrame(tdTable, columns = ['Percentile', 'Probability', '0-0', '1-0', 'Ratio', 'Credibility'])
    teDf = pd.DataFrame(teTable, columns = ['Percentile', 'Probability', '1-1', '0-1', 'Ratio', 'Credibility'])
    #print(tdDf.to_string())
    #print(teDf.to_string())

    print(tdDf.sort_values(by=['Credibility', 'Ratio'], ascending=[False, False]).head(5).to_string())
    print(teDf.sort_values(by=['Credibility', 'Ratio'], ascending=[False, False]).head(5).to_string())
    tdMinProbability = tdDf.sort_values(by=['Credibility', 'Ratio'], ascending=[False, False]).iat[0, 1]
    teMaxProbability = teDf.sort_values(by=['Credibility', 'Ratio'], ascending=[False, False]).iat[0, 1]

    print()
    print("0-0 size:" + str(data00Sets.shape[0]))
    print("1-0 size:" + str(data10Sets.shape[0]))
    print("0-1 size:" + str(data01Sets.shape[0]))
    print("1-1 size:" + str(data11Sets.shape[0]))
    
    print("td_min:" + str(tdMinProbability))
    print("td_max:" + str(tdMaxProbability))
    print("te_min:" + str(teMinProbability))
    print("te_max:" + str(teMaxProbability))
    
    
    f = open(save_place + "BEST THRESHOLD RESULTS.txt", "a")
    print("td_min:" + str(tdMinProbability), file=f)
    print("td_max:" + str(tdMaxProbability), file=f)
    print("te_min:" + str(teMinProbability), file=f)
    print("te_max:" + str(teMaxProbability), file=f)
    f.close()
    
    tdDf.sort_values(by=['Credibility', 'Ratio'], ascending=[False, False]).to_csv(save_place + "Thresholds_in_False_Negative_Data.csv")
    teDf.sort_values(by=['Credibility', 'Ratio'], ascending=[False, False]).to_csv(save_place + "Thresholds_in_False_Positive_Data.csv")
    
# if __name__ == "__main__":
    