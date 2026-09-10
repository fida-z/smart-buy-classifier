# %%
import pandas as pd
import numpy as np
from data_clean_exports import data

# %% [markdown]
# The clean data from the previous notebook has been imported to this notebook for the purpose of feature engineering.

# %%
data.head()

# %% [markdown]
# # Creating Features :

# %%
# Creating the car age feature :
data['car_age'] = 2026 - data['Make year']
data['reg_age'] = 2026 - data['Reg. year']


# %%
# creating NGT_life column

def ngt_life(fuel, car_age):
    if(fuel == 'Diesel'):
        return(10-car_age)
    elif(fuel == 'Electric'):
        return(15)
    else:
        return(15-car_age)

data['ngt_life'] = data.apply(lambda row: ngt_life(row['Fuel'], row['car_age']), axis=1)
data['ngt_critical'] = data['ngt_life'].map(lambda x: True if x<=3 else False) # binary column


# %% [markdown]
# In Delhi, Petrol vehicles are banned from being driven on roads after they reach an age of 15 years. For Diesel, the limit is 10 years. This is possibly a strong signal that can affect the price of a vehicle. Given two identical cars, the car with the greater NGT life is preferrable to a car with lower life simply because it can be driven for longer.
# 
# Electric vehicles have no NGT life ceiling, so their ngt_life has simply been set to 15, the maximum possible value.

# %%
data['frequency'] = data['model'].map(data['model'].value_counts())


# %%
data.info()

# %%
#RTO feature
data['re_register'] = ~(data['plate'].astype('str').str.contains('DL|Delhi|BH'))

# %% [markdown]
# This feature is created based on the hypothesis that a car registered outside Delhi may cost less than a car registered within Delhi, because a driver will have to re-register the car in Delhi before he can drive it within Delhi. 

# %%
# km_per_year column:
data['km_per_year'] = (data['KM driven']/data['car_age']).round(2)

# %% [markdown]
# Gives a measure of how much a car has actually been driven over the years. It is more explainable than two individual KM and Year columns.

# %%
# Luxury car brands :
luxury_cars = 'VOLVO|MERCEDES|AUDI|LEXUS|ROLLS-ROYCE|BENTLEY|PORSCHE|FERRARI|LAMBORGH|ASTON MARTIN|LAND ROVER|RANGE ROVER|BMW 7|BMW X7'
data['is_luxury_brand'] = data['model'].str.contains(luxury_cars)
data['is_luxury_brand'].value_counts()

# %% [markdown]
# Luxury car brands will have a higher degree of quality and price compared to other used cars.

# %%
data['ownership_strength'] = data['Ownership']/data['car_age']

# %%
data.columns

# %%
# Dividing the categorically encoded columns from the features column upto now :
enc = data.copy()



# %%
