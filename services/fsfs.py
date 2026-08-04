from core.setting import Base, engine
from models.orders import OrdersOrm

print(Base.metadata.tables)
Base.metadata.create_all(bind=engine, tables=[OrdersOrm.__table__])
print(Base.metadata.tables)
