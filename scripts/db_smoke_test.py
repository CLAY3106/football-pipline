#create_engine - creates a database connection factory
#text - safely wraps raw SQL strings so SQLAlchemy can execute them
from sqlalchemy import create_engine, text

#database connection url
db_url = "postgresql+psycopg2://football_user:football_pass@localhost:5432/football_dw"

#create sqlalchemy engine
engine = create_engine(db_url, future = True)

#open a database connection
with engine.connect() as conn:
    #query current database
    db = conn.execute(
        text("SELECT current_database()")
    ).scalar_one()

    #query current user
    user = conn.execute(
        text("SELECT current_user")
    ).scalar_one()

    #query schemas
    schemas = conn.execute(
        text("""
             SELECT schema_name
             FROM information_schema.schemata
             WHERE schema_name IN ('raw', 'staging', 'mart')
             ORDER BY schema_name
        """)
    ).all()

#print results
print("db:", db)
print("user:", user)
print("schemas:", [s[0] for s in schemas])
