import argparse,json
from pathlib import Path
import numpy as np,pandas as pd

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',default='data/processed/complaints.csv');p.add_argument('--embeddings',default='data/embeddings/complaint_embeddings.npy');args=p.parse_args()
 import hdbscan
 from sklearn.metrics import silhouette_score
 df=pd.read_csv(args.input);emb=np.load(args.embeddings);clusterer=hdbscan.HDBSCAN(min_cluster_size=3,metric='euclidean');labels=clusterer.fit_predict(emb);df['cluster_id']=labels
 Path('data/clusters').mkdir(parents=True,exist_ok=True);df.to_csv('data/clusters/clustered_complaints.csv',index=False)
 mask=labels>=0;metrics={'cluster_count':int(len(set(labels))- (1 if -1 in labels else 0)),'noise_percentage':float((labels==-1).mean()*100)}
 if mask.sum()>1 and len(set(labels[mask]))>1: metrics['silhouette_score']=float(silhouette_score(emb[mask],labels[mask]))
 Path('data/evaluations/clustering_metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
