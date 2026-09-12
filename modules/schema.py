from dataclasses import dataclass

@dataclass 
class UserCar:
    model: str
    fuel: str
    year: int
    transmission: str
    km_driven: int
    eng_capacity: int
    ownership: int
    asking_price: float

