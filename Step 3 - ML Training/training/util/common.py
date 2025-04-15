import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, make_scorer, precision_score, recall_score, average_precision_score, roc_auc_score, precision_recall_curve, auc, roc_curve, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
# from IPython.display import display


def anomaly_scores(original, transformed):
    sse = np.sum((original - transformed)**2, axis=1)
    return sse

def evaluate_results(y_true, score):
    precision, recall, threshold = precision_recall_curve(y_true, score, pos_label=None)
    au_precision_recall = auc(recall, precision)
    results = pd.DataFrame({'precision': precision, 'recall': recall})
    results["f1"] = 2*precision*recall/(precision+recall)
    results["f2"] = 5*precision*recall/(4*precision+recall)
    max_index_f1 = results["f1"].idxmax()
    max_index_f2 = results["f2"].idxmax()
    best = pd.concat([results.loc[max_index_f1], results.loc[max_index_f2]], keys= ["f1", "f2"])
    best["f1threshold"] = threshold[max_index_f1]
    best["f2threshold"] = threshold[max_index_f2]
    best["au_precision_recall"] = au_precision_recall
    fpr, tpr, thresholds = roc_curve(y_true, score, pos_label=-1)
    best["auroc"] = auc(fpr, tpr)
    return best

def evaluate_proba(y_true, score):
    precision, recall, threshold = precision_recall_curve(y_true, score, pos_label=1)
    results = pd.DataFrame({'precision': precision, 'recall': recall, 'threshold': np.append(threshold, np.inf)})
    best_index_fscore = {}
    f_scores = []
    for i in range(1, 10):
        results[f"F{i}"] = (1+i**2)*precision*recall/(i**2*precision+recall)
        best_index = results[f"F{i}"].idxmax()
        f_scores.append({
            "metric": f"F{i}", 
            "value": str(round(results[f'F{i}'][best_index], 4)), 
            "threshold": threshold[best_index],
            "precision": str(round(results["precision"][best_index], 4)),
            "recall": str(round(results["recall"][best_index], 4)),
            "FPR": (score[(y_true == 1)] >= threshold[best_index]).sum() / (y_true == 1).sum()
        })
    return results, pd.DataFrame(f_scores)

def plot_fscores(scores, summary, figsize=(10,6), min_recall=0.25, show_thresholds=False):
    n_points = sum(scores['recall'] >= min_recall)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(scores.loc[:n_points, 'threshold'], scores.loc[:n_points, 'recall'], label="recall", color="black")
    ax.plot(scores.loc[:n_points, 'threshold'], scores.loc[:n_points, 'precision'], label="precision", color="silver")
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
    n_curves = 0
    thresholds = []
    for f_col in scores.filter(regex="^F.+"):
        ax.plot(scores.loc[:n_points, 'threshold'], scores.loc[:n_points, f_col], label=f_col, color=colors[n_curves%len(colors)])
        ax.plot(float(summary.loc[summary.metric == f_col, "threshold"]), float(summary.loc[summary.metric == f_col, "value"]), marker="o", color=colors[n_curves%len(colors)])
        thresholds.append(float(summary.loc[summary.metric == f_col, "threshold"]))
        n_curves += 1
    if show_thresholds:
        for t in thresholds:
            ax.axvline(t, 0, 1, color="black", linestyle="--")
    ax.set_xlabel("threshold")
    ax.set_ylabel("value")
    plt.legend()
    return fig

def plot_confusion_matrix(y_true, y_pred, figsize=(7,7), cmap="Blues", values=[-1, 1], labels=["fraud", "benign"], title="", ax=None):
    cm = confusion_matrix(y_true, y_pred, labels=values)
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float)
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            annot[i, j] = '%.1f%%\n%d' % (p * 100, c)
    cm_perc = pd.DataFrame(cm_perc, index=labels, columns=labels)
    cm_perc.index.name = 'Actual'
    cm_perc.columns.name = 'Predicted'
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(cm_perc, cmap=cmap, annot=annot, fmt='', ax=ax, vmin=0, vmax=1)
    if title != "":
        ax.set_title(title)
    # fig.savefig(f'{save_place}' + 'test_after_training.png')
    # plt.savefig('/home/didik/Documents/cm.png')
    plt.show(block=True)
    return plt

