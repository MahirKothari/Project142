import pandas as pd
import numpy as np
df = pd.read_csv('articles.csv')
C= df['vote_average'].mean()
m = df['vote_count'].quantile(0.9)
q_articles = df.copy().loc[df['vote_count']>=m]
def weightedRating(x,m = m,C = C):
  v = x['vote_count']
  R = x['vote_average']
  return((v / (v+m)) * R + (m / (v+m)) * C)
q_articles['score'] = q_articles.apply(weightedRating,axis = 1)
q_articles = q_articles.sort_values('score',ascending = False)
output = q_articles[['url','title','text','lang','total_events']].head(20).values.tolist()