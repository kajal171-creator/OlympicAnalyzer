import pandas as pd

df = pd.read_csv(r'C:\Users\Kajal Mehra\Downloads\archive (62)\all_athlete_games.csv')
region_df = pd.read_csv(r'C:\Users\Kajal Mehra\Downloads\archive (62)\all_regions.csv')

def preprocess(df,region_df):
    #filtering for summer olympics
    df=df[df['Season']=='Summer']
    #merge with region_df
    df=df.merge(region_df,on='NOC',how='left')
    #dropping duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding medals
    df=pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df