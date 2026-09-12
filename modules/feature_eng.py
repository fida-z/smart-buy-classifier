import pandas as pd
import datetime

curr_year = datetime.date.today().year
LUXURY_MODELS = 'VOLVO|MERCEDES|AUDI|LEXUS|ROLLS-ROYCE|BENTLEY|PORSCHE|FERRARI|LAMBORGH|ASTON MARTIN|LAND ROVER|RANGE ROVER|BMW 7|BMW X7'


def calc_ngt_life(fuel: str, car_age: int) -> int:
    if(fuel == 'Diesel'):
        return(10-car_age)
    elif(fuel == 'Electric'):
        return(15)
    else:
        return(15-car_age)


def car_builder(carClass) -> pd.DataFrame :

    car_age = curr_year - carClass.year
    ngt_life = calc_ngt_life(carClass.fuel, car_age)
    ngt_critical = True if ngt_life<=3 else False
    is_lux_model = carClass.model in (LUXURY_MODELS)

    car_dict = {
        'model': carClass.model,
        'fuel': carClass.fuel, 
        'year': carClass.year, 
        'transmission': carClass.transmission, 
        'km_driven': carClass.km_driven, 
        'eng_capacity': carClass.eng_capacity, 
        'ownership': carClass.ownership, 
        'asking_price': carClass.asking_price,
        'car_age': car_age,
        'ngt_life': ngt_life,
        'ngt_critical': ngt_critical,
        'is_lux_model':  is_lux_model
    }
    car_df = pd.DataFrame([car_dict])
    car_df['model'] = car_df['model'].astype('category')
    car_df['fuel'] = car_df['fuel'].astype('category')
    car_df['transmission'] = car_df['transmission'].astype('category')

    return(car_df)

    
