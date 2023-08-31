import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer

from env import get_connection
import os

# Create helper function to get the necessary connection url.
def get_db_connection(database):
        return get_connection(database)

def acquire_zillow():
    # create helper function to get the necessary connection url.
    def get_db_connection(database):
        return get_connection(database)

    # connect to sql zillow database
    url = "zillow"

    # use this query to get data    
    sql_query = "SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips FROM properties_2017 WHERE propertylandusetypeid = 261"

    # assign data to data frame
    df = pd.read_sql(sql_query, get_connection(url))

    return df

def wrangle_zillow(df):
    # 1. Rename the columns to be more readable
    df = df.rename(columns = {'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':'area', 'taxvaluedollarcnt':'tax_value', 'yearbuilt':'year_built'})

    df = df.dropna()

    # 6. Convert data types
    df.bedrooms = df.bedrooms.astype('int')
    df.bathrooms = df.bathrooms.astype('int')
    df.area = df.area.astype('int')
    df.tax_value = df.tax_value.astype('int')
    df.year_built = df.year_built.astype('int')
    df.fips = df.fips.astype('int')

    # Save to csv
    df.to_csv('zillow_data.csv',index=False)
    
    return df


def scale_data(train, val, test, to_scale):
    #make copies for scaling
    train_scaled = train.copy()
    validate_scaled = val.copy()
    test_scaled = test.copy()

    #make the thing
    scaler = MinMaxScaler()

    #fit the thing
    scaler.fit(train[to_scale])

    #use the thing
    train_scaled[to_scale] = scaler.transform(train[to_scale])
    validate_scaled[to_scale] = scaler.transform(val[to_scale])
    test_scaled[to_scale] = scaler.transform(test[to_scale])
    
    return train_scaled, validate_scaled, test_scaled