import argparse
from pathlib import Path
import numpy as np,pandas as pd

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',default='data/embeddings/complaint_embeddings.npy');args=p.parse_args();
 from sentence_transformers import SentenceTransformer
 df=pd.read_csv(args.input);model=SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2');emb=model.encode(df['complaint_text'].fillna('').tolist(),normalize_embeddings=True,show_progress_bar=True);Path(args.output).parent.mkdir(parents=True,exist_ok=True);np.save(args.output,emb);print(f'Saved {len(emb)} embeddings to {args.output}')
if __name__=='__main__':main()
