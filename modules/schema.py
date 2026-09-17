from dataclasses import dataclass, field
import datetime

curr_year = datetime.date.today().year


@dataclass 
class UserCar:
    model: str
    fuel: str
    year: int
    transmission: str
    km_driven: float
    eng_capacity: float
    ownership: int
    asking_price: float
    car_age: int = field(init=False)
    def __post_init__(self):    
        self.car_age = curr_year - self.year

def submit_car(model, year, fuel, transmission, km_driven, engine_capacity, ownership, asking_price):
    numeric_fields = {
        'km_driven': km_driven, 
        'eng_capacity': engine_capacity, 
        'asking_price': asking_price
    }


    for field,value in numeric_fields.items():
        try:
            value = float(value)
        except:
            raise Exception(f'Invalid Datatype for {field} input!')

        
        if value < 0:
            raise Exception(f'{field} cannot be negative!')

        numeric_fields[field] = value
        

    return(UserCar(
        model=model,
        year=year,
        transmission=transmission,
        km_driven=numeric_fields['km_driven'],
        fuel=fuel,
        eng_capacity= numeric_fields['eng_capacity'],
        ownership=(ownership),
        asking_price=numeric_fields['asking_price']
    ))

