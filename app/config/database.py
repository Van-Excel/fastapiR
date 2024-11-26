import psycopg2
from psycopg2.extras import RealDictCursor

from app.config.settings import get_settings

# assign instance of settings config object to variable
settings = get_settings()


def get_DB_connection():

    try:

        # connect to postgres DB
        connection = psycopg2.connect(
            host=settings.host,
            database=settings.database,
            user=settings.user,
            password=settings.password,
            port=settings.port,
            cursor_factory=RealDictCursor,
        )

    # execute queries
    # cur.execute

    # retrieve results
    # records = cur.fetchall
    except Exception as error:
        print("connection to database failed")
        print("Error:", error)

    return connection



