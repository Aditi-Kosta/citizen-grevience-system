import argparse
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone
from ml.src.preprocessing.canonical import clean_text

CANON=['complaint_id','source_id','source_name','complaint_text','language','category','department','severity','urgency_score','location_text','latitude','longitude','submitted_at','status','is_duplicate','duplicate_of','cluster_id','classifier_confidence','classifier_model_version','embedding_model_version','created_at','updated_at']

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',default='data/processed/complaints.csv');args=p.parse_args();src=Path(args.input);df=pd.read_csv(src)
 text_col=next((c for c in ['complaint_text','text','complaint','description','narrative'] if c in df.columns),None)
 if not text_col: raise SystemExit('No complaint text column found. Expected complaint_text/text/complaint/description/narrative.')
 out=pd.DataFrame();out['complaint_text']=df[text_col].map(clean_text);out=out[out.complaint_text.str.len()>2].drop_duplicates('complaint_text').reset_index(drop=True)
 out['complaint_id']=[f'RAW-{i+1:06d}' for i in range(len(out))];out['source_id']='raw';out['source_name']=src.name
 for c in CANON:
  if c not in out: out[c]=None
 out['created_at']=datetime.now(timezone.utc).isoformat();out['updated_at']=out['created_at']
 Path(args.output).parent.mkdir(parents=True,exist_ok=True);out[CANON].to_csv(args.output,index=False);print(f'Wrote {len(out)} canonical complaints to {args.output}')
if __name__=='__main__':main()
