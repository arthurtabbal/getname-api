from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from urllib.parse import quote
from .db_config import DATABASE_CONFIGS
import os

# Get env variables
load_dotenv()

_engines = {}

FLASK_PORT = os.getenv("FLASK_PORT")

# Pool parameters
POOL_SIZE = os.getenv("POOL_SIZE")
POOL_MAX = os.getenv("POOL_MAX_OVERFLOW")
POOL_TIMEOUT = os.getenv("POOL_TIMEOUT")

QUERY = os.getenv("DB_QUERY")
MULTI_QUERY = os.getenv("DB_MULTI_QUERY")
NAME_QUERY = os.getenv("DB_NAME_QUERY")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET")

def get_engine(db_id: str):

    # 1. Check if this db_id is known
    if db_id not in DATABASE_CONFIGS:
        raise ValueError(f"Unknown database identifier: {db_id}")

    # 2. If engine already exists in the dictionary, return it
    if db_id in _engines:
        return _engines[db_id]

    # 3. Otherwise, read the DB config and create a new engine
    config = DATABASE_CONFIGS[db_id]

    TYPE = config["TYPE"]
    HOST = config["HOST"]
    DATABASE = config["DATABASE"]
    PORT = config["PORT"]
    USER = config["USER"]
    PASS = str(config["PASS"])

    if TYPE == "oracle":
        url_object = (
            f"oracle+cx_oracle://{USER}:{PASS}@{HOST}:{PORT}/?service_name={DATABASE}"
        )

    elif TYPE == "firebird":
        url_object = f"firebird+fdb://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}"

    elif TYPE == "mysql":
        url_object = f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}"

    else:
        TYPE = "mssql+pymssql" if TYPE == "mssql" else TYPE
        url_object = URL.create(
            TYPE, username=USER, password=PASS, host=HOST, database=DATABASE, port=PORT
        )

    engine = create_engine(
        url_object,
        pool_size=int(POOL_SIZE),
        max_overflow=int(POOL_MAX),
        pool_timeout=int(POOL_TIMEOUT),
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    # 4. Cache it in _engines
    _engines[db_id] = engine
    return engine
