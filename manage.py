import typer
import subprocess
from tqdm import tqdm
from pathlib import Path
from sqlalchemy import delete
from sqlalchemy.sql import text as stext
from main.main import create_dev_app
from main.db import Base,engine,db
from user.models import *
from store.models import *
from config import settings


capp = typer.Typer()
app=create_dev_app()

@capp.command()
def rung():
    """starts gunicorn server of the app with uvicorn works bound  to 0.0.0.0:8000 with one worker
    """
    subprocess.run(["gunicorn", "manage:app","-b" ,"0.0.0.0:8000","--reload","-w","1"]) 

@capp.command()
def upgrade():
    """creates  base models based on their metadata"""
    db.drop_all()
    db.create_all()

@capp.command()
def updatecontents():
    db.session.begin()
    db.session.execute(delete(ContentTypes))
    conts= [(x.split('_')[0],x) for x in Base.metadata.tables.keys() ]
    db.session.add_all([ContentTypes(app_label=x[0],model_name=x[1]) for x in conts ])
    db.session.commit()
@capp.command()
def dropall():
    db.drop_all()

@capp.command()
def test(location):
    """
      Takes location of test locations as arguments. this argument is required    
    """
    subprocess.run(["pytest", location,"--asyncio-mode=strict"])

@capp.command()
def usesql(): 
    # using sync sqlalchemy engine
    with engine.connect() as con:
         with open('flaskstore.sql') as f:
            for line in tqdm(f.readlines()):
                con.execute(stext(line))
  
                    
                
@capp.command()
def teststmt():
    pass
if __name__ == "__main__":
    capp()  