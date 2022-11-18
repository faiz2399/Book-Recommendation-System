import pandas as pd
import numpy as np
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from math import nan, isnan
from mlxtend.frequent_patterns import apriori
from sklearn.neighbors import NearestNeighbors
import pickle

df_final = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\final.xlsx')
df_des = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\final_with_Des.xlsx')
top_ten_ranked = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\tensorflow.xlsx')
df_rec = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\book_rec.xlsx')
df_book_filter = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\book_filter.xlsx')


def pop():
  R = df_final.groupby('Book-Title').mean().reset_index()[['Book-Title','Book-Rating']]
  R = R.rename(columns={'Book-Rating':'Avg-Rating'})
  df_pop = df_final.copy()
  df_pop['m'] = 50
  df_pop = pd.merge(df_pop, R, on = ['Book-Title'], how = 'left')
  df_pop['c'] = df_pop['Book-Rating'].mean()
  df_pop['Weighted-avg'] = df_pop['Book_Was_Rated']*df_pop['Avg-Rating']/(df_pop['Book_Was_Rated'] + df_pop['m']) + df_pop['m']*df_pop['c']/(df_pop['Book_Was_Rated'] + df_pop['m'])
  df_pop = df_pop.sort_values(by = 'Weighted-avg', ascending=False)
  df_pop = df_pop.drop(['Unnamed: 0', 'Book_Was_Rated','Avg-Rating','m','c'],axis = 1)
  df_pop = df_pop.rename(columns = {'Book-Title':'BookTitle','User-ID':'UserID','Image-URL-S':'ImageURL'})
  df_pop = df_pop.drop_duplicates('BookTitle')

#   df_pop = {'ImageURL':df_pop.head(10)['ImageURL'].to_list()}
 
  return df_pop.head(10)['ImageURL'].to_list()
def collab_filter(user_id):

  a = top_ten_ranked[top_ten_ranked['User-ID'] == user_id].sort_values(by='Book-Rating',ascending=False)
#   a = {'ImageTensor':a['Image-URL-S'].to_list()}
  return a['Image-URL-S'].to_list()
def knn(user_id):
    p = pd.pivot_table(df_final, values='Book-Rating', index='Book-Title', columns=['User-ID'])
    p_r = p.reset_index()
    d = p_r[p_r[user_id] > 0][[user_id,'Book-Title']]
    d =  pd.merge(d,df_book_filter, on='Book-Title',how = 'left')
  

    b = d['Book-Title'].to_list()
    k = df_rec.loc[df_rec['Book'].isin(b)]
    demo = pd.DataFrame({'Book-Title':list(np.unique(k[['Similar-book1', 'Similar-book2','Similar-book3','Similar-book4']].values))})
    demo = pd.merge(demo,df_book_filter, on='Book-Title',how = 'left')
  


    return d['Image-URL-S'].to_list(), demo['Image-URL-S'].to_list()
                
def user_item(user_id):
    p = pd.pivot_table(df_final, values='Book-Rating', index='Book-Title', columns=['User-ID']) 
    p = p.fillna(0)
    p_r = p.reset_index()
    f = open(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\distances.pckl', 'rb')
    distances = pickle.load(f)
    f.close()
    f = open(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\indices.pckl', 'rb')
    indices = pickle.load(f)
    f.close()
    read = []
    rec = []
    for m in p_r[p_r[user_id] > 0][user_id].index.tolist():
        read.append(m)
    for m in p_r[p_r[user_id] ==0][user_id].index.tolist():
        rec.append(m)
 
    sim_books = []
    sim_dists = []
    for i in rec:

        k = indices[i]
        d =distances[i]
        sim = []
        dist = []
        for j in range(0,k.shape[0]):
        
            sim.append(k[j])
            dist.append(d[j])
        
        sim_books.append(sim)
        sim_dists.append(dist)
    ratings = []
    df_new = df_final[df_final['User-ID']==user_id]
    for i in sim_books:
            r = []
            for j in i:
                b = p_r.iloc[j]['Book-Title']
                k = df_new[df_new['Book-Title']== b]['Book-Rating'].to_list()
                if len(k) >0:
                    r.append(k[0])
                else:
                    r.append(0)
            ratings.append(r)
    pred= []
    for i in range(len(sim_books)):
        pred.append(np.sum(np.array(sim_dists[i])*np.array(ratings[i]))/np.sum(sim_dists[i]))
    b_title = []
    for i in sim_books:
        b_title.append(p_r.iloc[i[0]]['Book-Title'])

    d_pred = pd.DataFrame({'Book':b_title,'Rating_pred':pred})
    d_pred = d_pred.sort_values(['Rating_pred'],ascending=False)
    d_pred = d_pred.drop_duplicates()
    d_pred = d_pred.rename(columns = {'Book':'Book-Title'})
    demo = pd.merge(d_pred,df_book_filter, on='Book-Title',how = 'left')

    return demo['Image-URL-S'].head(10).to_list()

  
    

# def content(user_id):
