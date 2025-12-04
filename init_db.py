from database import engine, SessionLocal, Base
from models import Product, Participant
import datetime

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Product).first():
        print("Database already initialized.")
        return

    # Create dummy products
    products = [
        Product(name="Milk", barcode="1001", price=2.50, stock_quantity=50, expiry_date=datetime.date.today() + datetime.timedelta(days=7)),
        Product(name="Bread", barcode="1002", price=1.20, stock_quantity=30, expiry_date=datetime.date.today() + datetime.timedelta(days=3)),
        Product(name="Apples", barcode="1003", price=0.50, stock_quantity=100, expiry_date=datetime.date.today() + datetime.timedelta(days=14)),
        Product(name="Yogurt", barcode="1004", price=0.99, stock_quantity=40, expiry_date=datetime.date.today() + datetime.timedelta(days=10)),
        Product(name="Cheese", barcode="1005", price=4.50, stock_quantity=20, expiry_date=datetime.date.today() + datetime.timedelta(days=30)),
        Product(name="Eggs", barcode="1006", price=3.00, stock_quantity=60, expiry_date=datetime.date.today() + datetime.timedelta(days=21)),
        # Expired items
        Product(name="Expired Milk", barcode="2001", price=1.00, stock_quantity=10, expiry_date=datetime.date.today() - datetime.timedelta(days=2)),
        Product(name="Old Bread", barcode="2002", price=0.50, stock_quantity=5, expiry_date=datetime.date.today() - datetime.timedelta(days=1)),
        Product(name="Rotten Apples", barcode="2003", price=0.10, stock_quantity=20, expiry_date=datetime.date.today() - datetime.timedelta(days=5)),
        Product(name="Sour Yogurt", barcode="2004", price=0.20, stock_quantity=15, expiry_date=datetime.date.today() - datetime.timedelta(days=3)),
    ]
    
    db.add_all(products)
    
    # Create dummy participants
    participants = [
        Participant(external_id="P-101", group_id="A"),
        Participant(external_id="P-102", group_id="B"),
        Participant(external_id="P-103", group_id="A"),
    ]
    
    db.add_all(participants)
    
    db.commit()
    db.close()
    print("Database initialized with dummy data.")

if __name__ == "__main__":
    init_db()
