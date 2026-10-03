from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def classification_metrics(y_true,y_pred):
    p,r,f,_=precision_recall_fscore_support(y_true,y_pred,average="macro",zero_division=0)
    wp,wr,wf,_=precision_recall_fscore_support(y_true,y_pred,average="weighted",zero_division=0)
    return {"accuracy":float(accuracy_score(y_true,y_pred)),"macro_precision":float(p),"macro_recall":float(r),"macro_f1":float(f),"weighted_f1":float(wf),"confusion_matrix":confusion_matrix(y_true,y_pred).tolist()}
