import os
from dotenv import load_dotenv
import reflex as rx

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

config = rx.Config(app_name="techmate_demo", db_url=DATABASE_URL)
