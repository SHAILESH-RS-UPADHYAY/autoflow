import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# The exact same connection string we put in mcp_config.json
DATABASE_URL = "postgresql://user:password@localhost:5432/autoflow"

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    signup_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

def setup_database():
    print(f"Connecting to PostgreSQL at {DATABASE_URL}...")
    engine = create_engine(DATABASE_URL)
    
    # Create tables
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Check if data exists
    if session.query(User).count() > 0:
        print("Mock data already exists in PostgreSQL. Skipping insertion.")
        return
        
    print("Generating mock data...")
    today = datetime.now()
    
    # Generate Users
    users = []
    for i in range(50):
        days_ago = random.randint(0, 30)
        signup_date = today - timedelta(days=days_ago)
        status = random.choice(['active', 'active', 'inactive'])
        users.append(User(name=f"User_{i}", signup_date=signup_date.date(), status=status))
    
    session.add_all(users)
    session.commit()
    
    # Generate Sales
    sales = []
    for _ in range(200):
        user_id = random.randint(1, 50)
        amount = round(random.uniform(10.0, 500.0), 2)
        days_ago = random.randint(0, 30)
        sale_date = today - timedelta(days=days_ago)
        sales.append(Sale(user_id=user_id, amount=amount, date=sale_date.date()))
    
    session.add_all(sales)
    session.commit()
    
    session.close()
    print("Mock data successfully injected into PostgreSQL!")

if __name__ == "__main__":
    setup_database()
