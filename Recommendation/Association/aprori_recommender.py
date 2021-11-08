def run(string):

    import pandas as pd
    import networkx as nx
    import plotly.express as px
    import matplotlib.pyplot as plt
    plt.style.use('default')
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    import os
    from pathlib import Path

    CUR_PATH = Path(__file__).resolve().parent

    CSV_FILE = os.path.join(CUR_PATH,'store_data1.csv')
    print("CSV_FILE",CSV_FILE)
    #Command for Powershell converting content of the file to lowercase
    #(Get-Content  "F:\mohit\ML\Amazon Recommendation System\Association\store_data0.csv" -Raw).ToLower() | Out-File "F:\mohit\ML\Amazon Recommendation System\Association\store_data0.csv" -Force
    df_orders = pd.read_csv(CSV_FILE)
    df_orders.shape

    df_orders = df_orders.replace(r'[^A-z0-9\n]+','_', regex=True)

    x = df_orders.to_string(header=False, index=False, index_names=False).split('\n')
    vals = [','.join(e.split()) for e in x]
    df_orders['combined'] = [','.join(e.split()) for e in x]

    df_orders_tmp = df_orders[['combined']].replace(to_replace=r',NaN.*$', value='', regex=True)

    df_orders_tmp['orderId'] = df_orders_tmp.index

    df_orders_tmp = df_orders_tmp.assign(combined=df_orders_tmp.combined.str.split(',')).explode('combined').reset_index(drop=True)
    df_orders_tmp = df_orders_tmp.replace(r'_',' ', regex=True)

    df_orders_tmp['itemQuantity'] = 1

    df = df_orders_tmp[['orderId','combined','itemQuantity']]
    df.columns = ['orderId','itemDescription','itemQuantity']
    print(df)

    #Visualisation
    df_table = df.copy()
    df_table['all'] = 'all'
    fig = px.treemap(df_table.head(30), path=['all', "itemDescription"], values='itemQuantity', color=df_table["itemQuantity"].head(30), hover_data=['itemDescription'], color_continuous_scale='Blues')
    #fig.show()

    print(df.value_counts())

    df_network = df.copy()
    df_network_first = df_network.groupby("itemDescription").sum().sort_values("itemQuantity", ascending=False).reset_index()
    df_network_first["itemType"] = "groceries"
    df_network_first = df_network_first.truncate(before=-1, after=15) # top 15
    plt.rcParams['figure.figsize']=(20,20)
    first_choice = nx.from_pandas_edgelist(df_network_first, source='itemType', target="itemDescription", edge_attr=True)
    pos = nx.spring_layout(first_choice)
    nx.draw_networkx_nodes(first_choice, pos, node_size=12500, node_color="lavender")
    nx.draw_networkx_edges(first_choice, pos, width=3, alpha=0.6, edge_color='black')
    nx.draw_networkx_labels(first_choice, pos, font_size=18, font_family='sans-serif')
    plt.axis('off')
    plt.grid()
    plt.title('Top 15 Products', fontsize=25)
    #plt.show()

    df_grouped = df.groupby(['orderId','itemDescription']).sum()['itemQuantity']
    df_basket = df_grouped.unstack().reset_index().fillna(0).set_index('orderId')

    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1
    basket_sets = df_basket.applymap(encode_units)
    print(basket_sets.head())

    #support > 0.5 is Good
    frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True).sort_values(by=['support'], ascending=False)
    #frequent_itemsets = apriori(basket_sets, min_support=0.05, use_colnames=True).sort_values(by=['support'], ascending=False)

    print("\n\nfrequent Itemset\n\n")
    print(len(frequent_itemsets))
    print(frequent_itemsets.head())

    rules = association_rules(frequent_itemsets, metric="lift")
    print(rules.head())

    print(rules[ (rules['lift'] > 1) & (rules['confidence'] >= 0.25) ])
    print(rules[['antecedents']])
    print(" - - - - - - - -")

    #if lift > 1 Good, confidence > 0.25
    data=rules[ (rules['lift'] > 1) & (rules['confidence'] >= 0.25) & (rules['antecedents']=={string}) ]
    print("SUGGESTION OF PRODUCT ",string)
    print(data['consequents'],type(data['consequents']))

    suggestions = []
    for i in data['consequents']:
        s=list(i)

        suggestions.append(s[0])

    print("suggestion in apriori",suggestions)
    return suggestions


if "__name__"=="__main__":
    #run("mobile")
    #print(run("pants"))
    pass
