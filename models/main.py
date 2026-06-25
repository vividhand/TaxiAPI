from core.setting import engine, Base
from DB.models.drivers import DriverOrm
from DB.models.cars import CarsOrm
from DB.models.users import UsersOrm
from DB.models.orders import OrdersOrm
from DB.models.reviews import ReviewsOrm
from DB.models.verify_email import EmailVerificationOrm
Base.metadata.create_all(engine)

