import numpy as np
import pandas as pd
import math
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import joblib
import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import warnings; warnings.simplefilter('ignore')#%matplotlib inline
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import csv
import os
from pathlib import Path


def updateData(lis):
    with open('','a') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(lis)
        f_object.close()

#document.getElementsByClassName('a-link-normal a-color-tertiary')
def prodDetail(ANSI):

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        source = requests.get(f"https://www.amazon.in/Samsung-Galaxy-Ocean-128GB-Storage/dp/{ANSI}/ref=sr_1_1_sspa?dchild=1&keywords=mobile&qid=1630244515&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExSVVKOFQ0OUc2ME40JmVuY3J5cHRlZElkPUEwMzEzMTU2MTRXSTdIT1BXUERPRCZlbmNyeXB0ZWRBZElkPUEwODE5NTkwMk82VFJWRTA5NFNJUSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=", headers = headers).text
        soup = BeautifulSoup(source, 'lxml')
        Category = []

        # print(soup.prettify())


        try:
                name=soup.find(id="productTitle")
                string = name.text
                name=string.strip()

                for i in soup.find_all('a', class_='a-link-normal a-color-tertiary'):
                    string = i.text
                    Category.append( string.strip())

                '''
                price=soup.find(id="priceblock_dealprice")
                string = price.text
                price=string.strip()
                price
                '''
                print("\nCategory :- ",Category)
                print(name)
        except Exception as e:
                pass
        #print(price)


def recommendPass(uid,num_rec):
    columns=['userId', 'productId', 'ratings','timestamp']

    CUR_PATH = Path(__file__).resolve().parent
    # CSV_FILE = os.path.join(CUR_PATH,'myfile.csv')
    CSV_FILE = os.path.join(CUR_PATH,'rating.csv')

    electronics_df=pd.read_csv(CSV_FILE,names=columns)

    # electronics_df=pd.read_csv('ratings_Electronics.csv',names=columns)

    electronics_df.drop('timestamp',axis=1,inplace=True)
    electronics_df.info()

    #Check the number of rows and columns
    rows,columns=electronics_df.shape
    print('Number of rows: ',rows)
    print('Number of columns: ',columns)

    #Check the datatypes
    electronics_df.dtypes


    #Taking subset of the dataset
    electronics_df1=electronics_df.iloc[:80,0:]

    electronics_df1.info()


    #Summary statistics of rating variable
    electronics_df1['ratings'].describe().transpose()


    #Find the minimum and maximum ratings
    print('Minimum rating is: %d' %(electronics_df1.ratings.min()))
    print('Maximum rating is: %d' %(electronics_df1.ratings.max()))


    #Check for missing values
    print('Number of missing values across columns: \n',electronics_df.isnull().sum())

    # Check the distribution of the rating
    with sns.axes_style('white'):
        g = sns.factorplot("ratings", data=electronics_df1, aspect=2.0,kind='count')
        g.set_ylabels("Total number of ratings")


    # Number of unique user id  in the data
    print('Number of unique users in Raw data = ', electronics_df1['userId'].nunique())
    # Number of unique product id  in the data
    print('Number of unique product in Raw data = ', electronics_df1['productId'].nunique())

    #Check the top 10 users based on ratings
    most_rated=electronics_df1.groupby('userId').size().sort_values(ascending=False)[:10]
    print('Top 10 users based on ratings: \n',most_rated)


    counts=electronics_df1.userId.value_counts()


    electronics_df1_final=electronics_df1[electronics_df1.userId.isin(counts[counts>=1].index)]
    print('Number of users who have rated 25 or more items =', len(electronics_df1_final))
    print('Number of unique users in the final data = ', electronics_df1_final['userId'].nunique())
    print('Number of unique products in the final data = ', electronics_df1_final['userId'].nunique())


    #constructing the pivot table
    final_ratings_matrix = electronics_df1_final.pivot(index = 'userId', columns ='productId', values = 'ratings').fillna(0)
    final_ratings_matrix.head()

    print('Shape of final_ratings_matrix: ', final_ratings_matrix.shape)

    #Calucating the density of the rating marix
    given_num_of_ratings = np.count_nonzero(final_ratings_matrix)
    print('given_num_of_ratings = ', given_num_of_ratings)
    possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]
    print('possible_num_of_ratings = ', possible_num_of_ratings)
    density = (given_num_of_ratings/possible_num_of_ratings)
    density *= 100
    print ('density: {:4.2f}%'.format(density))


    #Split the data randomnly into train and test datasets into 70:30 ratio
    train_data, test_data = train_test_split(electronics_df1_final, test_size = 0.3, random_state=0)
    train_data.head()

    '''
    print('Shape of training data: ',train_data.shape)
    print('Shape of testing data: ',test_data.shape)
    '''

    #Count of user_id for each unique product as recommendation score
    train_data_grouped = train_data.groupby('productId').agg({'userId': 'count'}).reset_index()
    train_data_grouped.rename(columns = {'userId': 'score'},inplace=True)
    train_data_grouped.head(40)


    #Sort the products on recommendation score
    train_data_sort = train_data_grouped.sort_values(['score', 'productId'], ascending = [0,1])

    #Generate a recommendation rank based upon score
    train_data_sort['rank'] = train_data_sort['score'].rank(ascending=0, method='first')

    #Get the top 5 recommendations
    popularity_recommendations = train_data_sort.head(5)
    popularity_recommendations

    # Use popularity based recommender model to make predictions
    def recommend(user_id):
        user_recommendations = popularity_recommendations

        #Add user_id column for which the recommendations are being generated
        user_recommendations['userId'] = user_id

        #Bring user_id column to the front
        cols = user_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendations = user_recommendations[cols]

        return user_recommendations


    # '''
    find_recom = [1,2,3]   # This list is user choice.
    for i in find_recom:
        print("The list of recommendations for the userId: %d\n" %(i))
        print(recommend(i))
        print("\n")
    # '''

    electronics_df_CF = pd.concat([train_data, test_data]).reset_index()
    electronics_df_CF.head()


    # Matrix with row per 'user' and column per 'item'
    pivot_df = electronics_df_CF.pivot(index = 'userId', columns ='productId', values = 'ratings').fillna(0)
    pivot_df.head()

    # print('Shape of the pivot table: ', pivot_df.shape)

    #define user index from 0 to 10
    pivot_df['user_index'] = np.arange(0, pivot_df.shape[0], 1)
    pivot_df.head()


    pivot_df.set_index(['user_index'], inplace=True)
    # Actual ratings given by users
    pivot_df.head()


    # Singular Value Decomposition
    U, sigma, Vt = svds(pivot_df, k = 10)

    '''
    print('Left singular matrix: \n',U)

    print('Sigma: \n',sigma)
    '''

    # Construct diagonal array in SVD
    sigma = np.diag(sigma)

    '''
    print('Diagonal matrix: \n',sigma)

    print('Right singular matrix: \n',Vt)
    '''

    #Predicted ratings
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)
    # Convert predicted ratings to dataframe
    preds_df = pd.DataFrame(all_user_predicted_ratings, columns = pivot_df.columns)
    preds_df.head()

    # Recommend the items with the highest predicted ratings

    def recommend_items(userID, pivot_df, preds_df, num_recommendations):
        # index starts at 0
        user_idx = userID-1
        # Get and sort the user's ratings
        sorted_user_ratings = pivot_df.iloc[user_idx].sort_values(ascending=False)
        #sorted_user_ratings
        sorted_user_predictions = preds_df.iloc[user_idx].sort_values(ascending=False)
        #sorted_user_predictions

        temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1)
        temp.index.name = 'Recommended Items'
        temp.columns = ['user_ratings', 'user_predictions']
        temp = temp.loc[temp.user_ratings == 0]
        temp = temp.sort_values('user_predictions', ascending=False)
        print('\nBelow are the recommended items for user(user_id = {}):\n'.format(userID))
        print(str(temp.head(num_recommendations)))

        s=temp.iloc[:num_rec,0]
        s = str(s)
        s = s.replace('Recommended Items','')
        s = s.replace('Name: user_ratings, dtype: float64','')
        s = s.replace('0.0','')
        s = s.replace('    ','')
        s = s.strip()
        s = s.split('\n')

        print('\n\n\n Recommended Items Names  ',s)
        return s
        #for i in s:
            #prodDetail(i)


    '''
    userID = 1
    num_recommendations = 5
    recommend_items(userID, pivot_df, preds_df, num_recommendations)

    userID = 2
    num_recommendations = 5
    recommend_items(userID, pivot_df, preds_df, num_recommendations)

    userID = 13
    num_recommendations = 5
    recommend_items(userID, pivot_df, preds_df, num_recommendations)
    '''
    # Actual ratings given by the users
    final_ratings_matrix.head()

    # Average ACTUAL rating for each item
    final_ratings_matrix.mean().head()

    # Predicted ratings
    preds_df.head()

    # Average PREDICTED rating for each item
    preds_df.mean().head()


    rmse_df = pd.concat([final_ratings_matrix.mean(), preds_df.mean()], axis=1)
    rmse_df.columns = ['Avg_actual_ratings', 'Avg_predicted_ratings']
    print(rmse_df.shape)
    rmse_df['item_index'] = np.arange(0, rmse_df.shape[0], 1)
    rmse_df.head()

    RMSE = round((((rmse_df.Avg_actual_ratings - rmse_df.Avg_predicted_ratings) ** 2).mean() ** 0.5), 5)
    print('\nRMSE SVD Model = {} \n'.format(RMSE))

    # Enter 'userID' and 'num_recommendations' for the user #
    userID = uid
    num_recommendations = num_rec
    return recommend_items(userID, pivot_df, preds_df, num_recommendations)

#prodDetail(str(B00001QHP5))
#prodDetail("B00000J061")
#B00001QHP5

if __name__=="__main__":
    pass
