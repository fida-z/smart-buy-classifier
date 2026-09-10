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
            
            if (file == '../scraped_data/data.txt'):
              main_dict['Source'] = 'Cars24'   
            else:
                main_dict['Source'] = 'CarDekho'

            df_list.append(main_dict)

df = pd.DataFrame(df_list)

# %% [markdown]
# The data for this project has been scraped from both Cars24 and CarDekho. Both have been stored in two seperate .txt files, 'data.txt' and 'cardekho.txt', in different ways. Each line of the .txt file is a python dictionary that stores relevant information about the car. The above function reads in each line, converts it to a dictionary, and appends it to a list of dictionaries. This list is then converted into a dataframe df.

# %% [markdown]
# # Basic Overview of the Data

# %%
df.head()

# %%
print(f"There are {df.shape[0]} rows and {df.shape[1]} columns in the dataset.")

# %%
print(f"There are {df.duplicated().value_counts().iloc[1]} duplicated rows.")

# %% [markdown]
# Since the data has been scraped over multiple days, the same listings get captured by the scraper. Additionally, CarDekho also lists some cars found on Cars24, which could be contributing to the number of duplicates.

# %% [markdown]
# # Modifying Datatypes :

# %%
df.info()

# %% [markdown]
# Almost all rows are of an incorrect datatype. THis is to be rectified. Many rows are also null, some having so few values that using them for any meaningful analysis is almost impossible. They are to be dropped. 
# 
# Certain information given by Cars24 about cars is not present in CarDekho. For example, `Spare key` and `Reg number` are not provided on CarDekho, which explains their equal number of missing values. 
# 
# Insurance and Insurance type have inconsistent number of nulls, even though they are related to each other. One reason for this is the CarDekho-v/s-Cars24 missing data mentioned in the previous line.

# %%
# creating a copy:
data = df.copy()

# %%
# Modifying Ownership :
maps = {'1st':1, '2nd':2, '3rd':3, '4th':4, '5th': 5, '6th':6, '7th':7, 
        'First Owner':1, 'Second Owner':2, 'Third Owner':3, 'Fourth Owner':4, 'Fifth Owner':5}
data['Ownership'] = data['Ownership'].replace(maps)

# %%
# function to parse car model column :
import re
def parse_model(x):

    x = x.upper()

    if(x.find('\n') != -1):  # cardekho cars
        temp_split = x.split('\n')
        model = temp_split[0].split(' ')
        variant = temp_split[1]

        if(model[0].isdigit() and len(model[0]) == 4):  # parsing the model name
            model = model[1:]
        else:
            model = model[0:]
        
        if(model[1] == 'SUZUKI'):
            del model[1]

        garbages = ['PETROL','CNG','DIESEL', 'AT', 'MT', 'AMT']   # removing fuel description from variant
        for garbage in garbages:
            if(garbage in variant):
                variant = variant.replace(garbage,'')
        
        variant = re.sub(r'\d\.\d[L]?', '', variant)    

        model = ' '.join(model).strip()
        
    else:  # cars24 cars
        if('NEW' in x):
            x = x.replace('NEW','')

        temp_split = x.split(' ')
        for i in range(len(temp_split) - 1):  # cleaning up extra ''s
            if(temp_split[i] == ''):
                del temp_split[i]

        if(temp_split[2] == 'GRAND' or temp_split[2] == 'WAGON'):
            model = temp_split[1]+" "+temp_split[2]+' '+temp_split[3]
            variant = ' '.join(temp_split[4:])
        else:
            model = temp_split[1]+' '+temp_split[2]
            variant = ' '.join(temp_split[3:]).strip()
        
        garbages = ['PETROL','CNG','DIESEL', ' AT', ' MT', ' AMT', ' I-VTEC']   # removing fuel description from variant
        for garbage in garbages:
            if(garbage in variant):
                variant = variant.replace(garbage,'')
        
        variant = re.sub(r'\d\.\d[L]?', '', variant)   
    return(model,variant)


# %%
# trimming model column :
data[['model','variant']] = data['model'].apply(lambda x: pd.Series(parse_model(x)))
data['model'].value_counts()[:10] 

# %%
data.head()

# %% [markdown]
# The original `model` column of the car included a lot of redundant information such as the year, fuel-type, etc. that already have dedicated columns for it. Hence, these components are dropped. Readability has also improved.
# 
# One problem that arose here is that Maruti Swift and Maruti Suzuki Swift were being errenuosly considered to be separate vehicles despite the fact that they are the same. This edge case is also handled.

# %%
data.head()

# %%
# replacing price column :
def price_conversion(x):
    x = x.lower().replace('₹','')

    if(x.endswith('lakh')):
        x = x.replace('lakh','')
        x = float(x)*100000

    elif(x.endswith('crore')):
        x = x.replace('crore', '')
        x = float(x)*10000000
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

# %% [markdown]
# This change only keeps the basic price evaluation label of the Cars24 listing, improving readability.

# %%
# converting Reg. year and Make year
data['Reg. year'] = pd.to_datetime(data['Reg. year']).dt.year
data['Make year'] = pd.to_datetime(data['Make year']).dt.year

# %% [markdown]
# The Year columns, previously stored as objects have been converted to datetime objects.

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

# %% [markdown]
# `Insurance type` is a meaningful attribute of a vehicle. If a seller does not provide Insurance information while selling their car, it might be a red flag. A relatively new car of a top-tier model not having insurance information is curious, and it might be a genuine signal that can be picked up by an ML model. Hence, instead of dropping the whole column altogether, the nulls have been replaced with `Unknown`.

# %%
# Replacing Engine capacity with other cars of the same make :
data['Engine capacity'] = data['Engine capacity'].fillna(
    data.groupby(['model', 'variant'])['Engine capacity'].transform('mean'))

# %%
data[data['Engine capacity'].isna()]

# %%
# for cars where model + year are too limiting :

data['Engine capacity'] = data['Engine capacity'].fillna(
    data.groupby('model')['Engine capacity'].transform('median')
)

# %%
data[data['Engine capacity'].isna()]

# %%
data.loc[data['Engine capacity'].isna(),'Engine capacity'] = 0
# %% [markdown]
# Cars belonging to the same year-model combination are almost certain to have the same engine capacities. Hence, they have been interpolated. 
# 
# Still, the above imputation method still left some nulls. These vehicles where simply imputed with the median engine capacity for their specific model. This is likely to be less accurate. 
# 
# Cars that still had null values were EVs, which do not have engine capacities in the first place. They were replaced with 0.

# %% [markdown]
# # Dropping Unnecessary Rows and Columns :

# %%
data.drop_duplicates(inplace=True, keep='first')
print(f"After dropping duplicates, {data.shape[0]} rows remain.")

# %%
del data['Reg number']
del data['Spare key']
del data['Insurance']

# %%
data.head()


