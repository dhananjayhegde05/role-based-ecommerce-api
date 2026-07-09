from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://dhananjayhegde@localhost:5432/ecommerce_db"

engine = create_engine(DATABASE_URL)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        print(result.fetchone())