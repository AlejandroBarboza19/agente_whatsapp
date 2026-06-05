from langchain_community.utilities import SQLDatabase
from app.core.config import settings

db_url = settings.database_url

db_for_agent = SQLDatabase.from_uri(db_url)