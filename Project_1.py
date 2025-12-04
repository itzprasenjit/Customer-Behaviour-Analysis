import pandas as pd;

df=pd.read_csv("customer_shopping_behavior.csv")

# print(df.head())
# print(df.info())
# print(df.describe()) for only numeric value
# print(df.describe(include='all'))

# print(df.isnull().sum()) review has 37 null value which should be replaced by median val




df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
# print(df.isnull().sum()) review na problem solved




# comumn name is upper case and lower case with spacing but it causes difficulty so we conver it to snake casing ie(all small letter by underscore)

df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
# print(df.info()) every thing is ok except purchase_amout_(usd) so replce the name 
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
# print(df.info()) snamke casing done


# create a age_group column
labels=['Young Adult', 'Adult', 'Middle-aged','Senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
# print(df[['age','age_group']].head())



#create column purchase_frquency_days as purchase frequency is given in text format ie(quaterly,weakly...) and analysing tetual data is complicated so convert it into numerical data

frequency_mapping={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}

df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
# print(df[['purchase_frequency_days','frequency_of_purchases']].head(30))



#promo code used and discount comumn contain same info so we dont need both the column
# print((df['discount_applied']==df['promo_code_used']).all()) to check
df=df.drop('promo_code_used',axis=1)




df.to_csv("customer_shopping_behavior_cleaned.csv", index=False)




from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "pass786171"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df=df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
print(pd.read_sql("SELECT * FROM customer LIMIT 5;", engine))
