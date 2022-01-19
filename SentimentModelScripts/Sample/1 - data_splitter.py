# Take Data After Cleaning and Clustering - Split it into 7 parts for manual labelling.
import pandas

df2 = pd.read_csv('Data/WSB_Comments_Clean_wClusters_Reduced.csv')


df2['Date']=pd.to_datetime(df2['Date Posted'])

months = [g for n, g in df2.groupby(pd.Grouper(key='Date',freq='M'))]



Ayman = months[7].sample(250).append(months[8].sample(250))


Ayman = Ayman.to_csv('Sample/Raw/Ayman.csv')
