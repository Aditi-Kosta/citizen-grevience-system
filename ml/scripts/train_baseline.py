import argparse,json,joblib
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from ml.src.classification.baseline import build

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--text-column',default='complaint_text');p.add_argument('--label-column',default='category');args=p.parse_args()
 df=pd.read_csv(args.input);df=df[[args.text_column,args.label_column]].dropna();df[args.text_column]=df[args.text_column].astype(str).str.strip();df=df[df[args.text_column].str.len()>2]
 Xtr,Xtmp,ytr,ytmp=train_test_split(df[args.text_column],df[args.label_column],test_size=.30,random_state=42,stratify=df[args.label_column]);Xv,Xte,yv,yte=train_test_split(Xtmp,ytmp,test_size=.50,random_state=42,stratify=ytmp)
 model=build();model.fit(Xtr,ytr);pred=model.predict(Xte);report=classification_report(yte,pred,output_dict=True,zero_division=0)
 out=Path('data/evaluations');out.mkdir(parents=True,exist_ok=True);Path('models/baseline').mkdir(parents=True,exist_ok=True)
 metrics={'accuracy':report['accuracy'],'macro_precision':report['macro avg']['precision'],'macro_recall':report['macro avg']['recall'],'macro_f1':report['macro avg']['f1-score'],'weighted_f1':report['weighted avg']['f1-score'],'per_class':{k:v for k,v in report.items() if isinstance(v,dict)},'split':{'train':len(Xtr),'validation':len(Xv),'test':len(Xte)}}
 (out/'baseline_metrics.json').write_text(json.dumps(metrics,indent=2));joblib.dump({'model':model,'labels':list(model.classes_)},'models/baseline/classifier.joblib');print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
