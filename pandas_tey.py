import pandas as pd
def addhazem(name):
    return name+"hazem"
        
data=pd.read_csv(r"C:\Users\PCS\Desktop\data_collection\ramen-ratings.csv")
data1=data.aggregate({"Brand":addhazem})
print(data1.head(10))
