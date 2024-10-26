from fastapi import FastAPI
from database import engine, Base, get_db




app = FastAPI()

@app.get('/')
def index():
    return 'hello'
# models.Base.metadata.create_all(bind=engine)

  