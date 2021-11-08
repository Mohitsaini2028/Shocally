


# links
'''
https://www.kaggle.com/shawamar/product-recommendation-system-for-e-commerce
https://www.kaggle.com/c/home-depot-product-search-relevance/data?select=test.csv.zip
'''

def run(string):
    import pandas as pd
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.neighbors import NearestNeighbors
    from sklearn.cluster import KMeans
    from sklearn.metrics import adjusted_rand_score
    import os
    from pathlib import Path
    CUR_PATH = Path(__file__).resolve().parent
    CSV_FILE = os.path.join(CUR_PATH,'prod_Desc.csv')
    product_descriptions = pd.read_csv(CSV_FILE)
    print(product_descriptions.shape)

    product_descriptions = product_descriptions.dropna()
    product_descriptions.shape
    product_descriptions.head()

    product_descriptions1 = product_descriptions.head(500)
    # product_descriptions1.iloc[:,1]

    product_descriptions1["product_description"].head(10)

    vectorizer = TfidfVectorizer(stop_words='english')
    X1 = vectorizer.fit_transform(product_descriptions1["product_description"])
    X1
    X=X1

    kmeans = KMeans(n_clusters = 10, init = 'k-means++')
    y_kmeans = kmeans.fit_predict(X)
    plt.plot(y_kmeans, ".")
    #plt.show()
    clus = []
    def print_cluster(i):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
            clus.append(terms[ind])
        print

    # # Optimal clusters is

    true_k = 10

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X1)


    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    #for i in range(true_k):
    #    print_cluster(i)


    def show_recommendations(product):
        #print("Cluster ID:")
        Y = vectorizer.transform([product])
        prediction = model.predict(Y)
        #print(prediction)
        print_cluster(prediction[0])

        return clus;


    return show_recommendations(string)

if __name__=="__main__":
    print(" -  - -  -  - - - -  - - - -  - -")
