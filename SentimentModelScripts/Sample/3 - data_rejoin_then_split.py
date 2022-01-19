# Round 2 labelling - select a new sample to be labelled (remove previously labelled data)

import pandas as pd
import os
import re
os.chdir('''Team_094\\SentimentModelScripts''')

df2 = pd.read_csv('Sample/Labelled/Ayman.csv')


df = pd.concat([df1,df2,df3,df4,df5,df6])



df = df[['Comment','ProcessedComments', 'HumanSentiment']]




df['HumanSentiment']=df['HumanSentiment'].str.replace(r'\bg\b','positive')\
                                         .str.replace(r'\bn\b','negative')\
                                         .str.replace(r'\bne\b','negative')\
                                         .str.replace(r'\bneg\b','negative')\
                                         .str.replace(r'\bb\b','negative')\
                                         .str.replace(r'\bneu\b','neutral')\
                                        .str.replace(r'\bnetural\b','neutral')\
                                        .str.replace(r'\bneu\b','neutral')\
                                        .str.replace(r'\bpos\b','positive')\
                                        .str.replace(r'\boos\b','positive')\
                                        .str.replace(r'\bPositive\b','positive')
#df = pd.read_csv('Outputs/WSB_Comments_Clean_wClusters.csv')
df = df.fillna('positive')

df.HumanSentiment.value_counts()



def text_clean(comments):
    features = []
    for comment in range(0, len(comments)):
        # Replace ' with ''
        processed = (str(comments[comment])).replace("’","")
        processed = processed.replace("'","")

        # Remove all the special characters
        processed = re.sub(r'\W', ' ', processed)

        # Remove all single characters
        #processed= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed)

        # Remove single characters from the start
        #processed = re.sub(r'\^[a-zA-Z]\s+', ' ', processed)

        # Substituting multiple spaces with single space
        processed = re.sub(r'\s+', ' ', processed, flags=re.I)

        # Trim text
        processed = processed.strip()

        # Converting to Lowercase
        #processed = processed.lower()
        features.append(processed)
    return features

features = df.iloc[:,1].values
processed_features = text_clean(features)
df['ProcessedComments'] = processed_features

df = df.drop(df[df['ProcessedComments'] == 'deleted'].index)


df_org = pd.read_csv('Outputs/WSB_Comments_Clean_wClusters_Reduced.csv')

df_org2 = pd.merge(df_org, df, how='left', left_index=True, right_index=True)

df_org2 = df_org2[~df_org2.index.duplicated(keep='first')]

df_org2.HumanSentiment_y.value_counts()

df_org2 = df_org2[~df_org2['HumanSentiment_y'].notnull()]


df_org2 = df_org2.drop(columns=['Comment_y', 'ProcessedComments_y', 'HumanSentiment_y'])

df_org2 = df_org2.rename(columns={'Comment_x': 'Comment', 'ProcessedComments_x': 'ProcessedComments', 'HumanSentiment_x': 'HumanSentiment'})

df_org2['Date']=pd.to_datetime(df_org2['Date Posted'])

months = [g for n, g in df_org2.groupby(pd.Grouper(key='Date',freq='M'))]



Ayman = months[7].sample(250).append(months[8].sample(250))



Ayman = Ayman.to_csv('Sample/Labelled/Round2/Ayman_R2.csv')


#df.to_csv('Sample/Labelled/data_round2.csv')
