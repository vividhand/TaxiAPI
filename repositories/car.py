from core.setting import engine
from models.cars import CarsOrm
from sqlalchemy.orm import Session
class CarRepositories:
    def __init__(self):
        self.session = Session(engine)
    def add_car(self, driver_id: str, plate_number: str, brand: str, look: str):
        try:
            with self.session as sess:
                new_car = CarsOrm(driver_id=driver_id, plate_number=plate_number, brand=brand, look=look)
                sess.add(new_car)
                sess.commit()
                return True
        except Exception as e:
            return [False, e]