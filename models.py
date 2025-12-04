from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Product(Base):
    """
    Represents a product in the supermarket inventory.
    
    Attributes:
        id (int): Unique identifier.
        name (str): Name of the product.
        barcode (str): Unique barcode string (scanned by POS).
        price (float): Unit price of the product.
        stock_quantity (int): Current stock level.
        expiry_date (Date): Expiration date for freshness checks.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    barcode = Column(String, unique=True, index=True)
    price = Column(Float)
    stock_quantity = Column(Integer)
    expiry_date = Column(Date)

class Participant(Base):
    """
    Represents a research participant or shopper.
    
    Attributes:
        id (int): Unique identifier.
        external_id (str): Public ID used for login (e.g., "P-101").
        group_id (str): Research group assignment (e.g., "Control", "Intervention").
    """
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    group_id = Column(String)

class Transaction(Base):
    """
    Represents a completed shopping session (checkout).
    
    Attributes:
        id (int): Unique identifier.
        participant_id (int): Foreign key to the Participant.
        timestamp (DateTime): When the transaction occurred.
        total_amount (float): Total cost of the transaction.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float)

    participant = relationship("Participant")
    items = relationship("TransactionItem", back_populates="transaction")

class TransactionItem(Base):
    """
    Represents a specific item purchased within a transaction.
    
    Attributes:
        id (int): Unique identifier.
        transaction_id (int): Link to the parent Transaction.
        product_id (int): Link to the Product purchased.
        quantity (int): Number of units purchased.
        price_at_purchase (float): Price per unit at the time of purchase (for historical accuracy).
    """
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_purchase = Column(Float)

    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product")

