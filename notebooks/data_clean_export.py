# %%
import pandas as pd
import numpy as np

# %% [markdown]
# ### Function to read the .txt files into a DataFrame

# %%

df_list = []
file_locs = ['../scraped_data/data.txt','../scraped_data/cardekho.txt']
for file in file_locs:
    with open(file, 'r', encoding='utf-8') as rf:
        for line in rf:
            inp = eval(line)
            main_dict = {}

            for key, value in inp.items():
                if(key == 'info'):
                    for keyinfo,valueinfo in inp[key].items():
                        main_dict[keyinfo] = valueinfo   
                else:
                        main_dict[key] = value
            df_list.append(main_dict)

df = pd.DataFrame(df_list)

# %% [markdown]
# # Basic Overview of the Data

# %%
df.head()

# %%
print(f"There are {df.duplicated().value_counts().iloc[1]} duplicated rows.")

# %% [markdown]
# # Modifying Datatypes :

# %%
df.info()

# %%
df.head()

# %% [markdown]
# - `model` to only include the main name of the model. 
# - `price`, `KM driven` and `Engine capacity` to be converted into a numeric format
# - `price_score` to be trimmed down.
# - `plate` to be standardised.
# - `Reg year` and `Make year` to be converted into datetime objects.
# 

# %%
# creating a copy:
data = df.copy()

# %%
# trimming model column :
data['model'] = data['model'].str.upper()
data['model'] = data['model'].str.replace('\n',' ') # cleaning up the newlines
data['model'] = data['model'].str.split(' ').map(lambda x: x[1]+' '+x[2] if x[2] != 'Suzuki' else x[1]+' '+x[2]+' '+x[3])
data['model'].value_counts()[:10] # FIX MAruti SUZUKI

# %%
# replacing price column :
def price_conversion(x):
    x = x.lower().replace('₹','')

    if(x.endswith('lakh')):
        x = x.replace('lakh','')
        x = float(x)*100000

    elif(x.endswith('thousand')):
        x = x.replace('thousand','')
        x = float(x)*1000
    
    return(x)

data['price'] = data['price'].map(price_conversion)

# %%
# converting KM driven and engine capacity column:
data['KM driven'] = data['KM driven'].str.replace(r'[A-Za-z,\s]+', '', regex=True).astype('int')
data['Engine capacity'] = data['Engine capacity'].str.strip().str.replace('cc','').astype('Float64')


# %%
# trimming price_score column :
data['price_score'] = data['price_score'].replace('NA', np.nan)
data.loc[data['price_score'].notna(), 'price_score'] = data.loc[data['price_score'].notna(), 'price_score'].str.split(' ').map(lambda x: x[0]+' '+x[1])

# %%
# converting Reg. year and Make year
data['Reg. year'] = pd.to_datetime(data['Reg. year']).dt.year
data['Make year'] = pd.to_datetime(data['Make year']).dt.year

# %%
# map plates :
data['plate'].value_counts()
data['plate'] = data['plate'].replace(r'[0-9-]+','', regex=True)
mappings = {'DL':'New Delhi', 'DLC':'New Delhi', 'UP':'Uttar Pradesh', 'Noida':'Uttar Pradesh', 
            'HR':'Haryana', 'Gurgaon':'Haryana', 'Faridabad':'Haryana', 'Ghaziabad':'Uttar Pradesh',
            'ballabhgarh': 'Haryana', 'UK':'Uttarakhand', 'Lucknow':'Uttar Pradesh', 'palwal':'Haryana'
            ,'BH':'Bharat','RJ':'Rajasthan','PB':'Punjab'}
print(data['plate'].replace(mappings).value_counts()[:100])

# %% [markdown]
# # Examining Nulls :

# %%
df.isna().sum()

# %% [markdown]
# - `Spare Key` and `Reg Number` both have same number of null values, because they have been sourced from CarDekho, which does not provide this info.
# - `price_score` field will have more nulls than depicted, because this info is not given in the CarDekho records either.
# - `Engine capacity` nulls can be interpolated from other cars of the same model.
# - `Insurance type` has less number of nulls than `Insurance`, because CarDekho data doesn't provide data for the 'Insurance' column.

# %%
# Replacing Insurance type nulls w/ unknown:
data.loc[data['Insurance type'].isna(),'Insurance type'] = 'Unknown'

# %%
# Replacing Engine capacity with other cars of the same make :
data['Engine capacity'] = data['Engine capacity'].fillna(
    data.groupby(['model', 'Make year'])['Engine capacity'].transform('mean'))

# %%
# for cars where model + year are too limiting :

data['Engine capacity'] = data['Engine capacity'].fillna(
    data.groupby('model')['Engine capacity'].transform('mean')
)

# %%
data[data['Engine capacity'].isna()]

# %% [markdown]
# There is a sparsity of data for the above models, meaning that no accurate model can be created for them.

# %% [markdown]
# # Dropping Unnecessary Rows and Columns :

# %%
data.drop_duplicates(inplace=True, keep='first')
data.shape[0]

# %%
del data['Reg number']
del data['Spare key']
del data['Insurance']

# %%
data.head()

# %%


