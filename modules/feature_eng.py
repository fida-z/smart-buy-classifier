import pandas as pd

LUXURY_MODELS = 'VOLVO|MERCEDES|AUDI|LEXUS|ROLLS-ROYCE|BENTLEY|PORSCHE|FERRARI|LAMBORGH|ASTON MARTIN|LAND ROVER|RANGE ROVER|BMW 7|BMW X7'


def calc_ngt_life(fuel: str, car_age: int) -> int:
    if(fuel == 'Diesel'):
        return(10-car_age)
    elif(fuel == 'Electric'):
        return(15)
    else:
        return(15-car_age)


def car_builder(carClass) -> pd.DataFrame :

    car_age = carClass.car_age
    ngt_life = calc_ngt_life(carClass.fuel, carClass.car_age)
    ngt_critical = True if ngt_life<=3 else False
    is_lux_model = carClass.model in (LUXURY_MODELS)

    car_dict = {
        'model': carClass.model,
        'Fuel': carClass.fuel, 
        'year': carClass.year, 
        'Transmission': carClass.transmission, 
        'KM driven': carClass.km_driven, 
        'Engine capacity': carClass.eng_capacity, 
        'Ownership': carClass.ownership, 
        'asking_price': carClass.asking_price,
        'car_age': car_age,
        'ngt_life': ngt_life,
        'ngt_critical': ngt_critical,
        'is_luxury_brand':  is_lux_model
    }
    car_df = pd.DataFrame([car_dict])
    car_df['model'] = car_df['model'].astype('category')
    car_df['Fuel'] = car_df['Fuel'].astype('category')
    car_df['Transmission'] = car_df['Transmission'].astype('category')

    return(car_df)

    
