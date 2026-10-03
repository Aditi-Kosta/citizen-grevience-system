"""Optional DistilBERT fine-tuning entry point.

This is not run during normal application startup. Install ml/requirements-optional.txt first.
"""
import argparse, json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--text-column',default='complaint_text'); p.add_argument('--label-column',default='category'); p.add_argument('--output',default='models/classifier'); p.add_argument('--epochs',type=int,default=2); args=p.parse_args()
    try:
        from datasets import Dataset
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
    except ImportError as e:
        raise SystemExit('Install ml/requirements-optional.txt before transformer training.') from e
    df=pd.read_csv(args.input)[[args.text_column,args.label_column]].dropna(); df[args.text_column]=df[args.text_column].astype(str)
    labels=LabelEncoder().fit(df[args.label_column].astype(str)); df['label']=labels.transform(df[args.label_column].astype(str)); train,test=train_test_split(df,test_size=.15,random_state=42,stratify=df['label']); train,val=train_test_split(train,test_size=15/85,random_state=42,stratify=train['label'])
    model_name='distilbert-base-uncased'; tokenizer=AutoTokenizer.from_pretrained(model_name)
    def tok(batch): return tokenizer(batch[args.text_column],padding='max_length',truncation=True,max_length=128)
    def ds(x): return Dataset.from_pandas(x[['%s'%args.text_column,'label']]).map(tok,batched=True).remove_columns([args.text_column,'__index_level_0__'] if '__index_level_0__' in Dataset.from_pandas(x[['%s'%args.text_column,'label']]).column_names else [args.text_column])
    dtrain,dval,dtest=ds(train),ds(val),ds(test); n=len(labels.classes_); model=AutoModelForSequenceClassification.from_pretrained(model_name,num_labels=n)
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    training=TrainingArguments(output_dir=str(out/'checkpoints'),num_train_epochs=args.epochs,per_device_train_batch_size=8,per_device_eval_batch_size=16,evaluation_strategy='epoch',save_strategy='epoch',load_best_model_at_end=True,report_to=[])
    trainer=Trainer(model=model,args=training,train_dataset=dtrain,eval_dataset=dval,tokenizer=tokenizer); trainer.train(); trainer.save_model(out); tokenizer.save_pretrained(out)
    (out/'label_mapping.json').write_text(json.dumps({str(i):c for i,c in enumerate(labels.classes_)},indent=2)); (out/'metadata.json').write_text(json.dumps({'model_version':'classifier-v1','base_model':model_name,'num_classes':n,'dataset_version':'v1'},indent=2)); print(f'Saved transformer model to {out}')
if __name__=='__main__': main()
