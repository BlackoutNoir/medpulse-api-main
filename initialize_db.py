from database import engine, Base
from models import *

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


#create and admin some of the default objects(pages for booking appointments, allergies and diagnosis)