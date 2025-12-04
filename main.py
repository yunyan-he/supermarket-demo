from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Generator
import models, schemas
from database import SessionLocal, engine
import pandas as pd
import io

app = FastAPI(
    title="Lab Supermarket POS System",
    description="Backend API for the experimental supermarket POS system.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

# Dependency
def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency generator.
    Yields a database session and ensures it closes after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """
    Serves the main POS interface (Point of Sale).
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        TemplateResponse: Renders `index.html`.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def read_admin(request: Request):
    """
    Serves the Research Dashboard (Admin UI).
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        TemplateResponse: Renders `admin.html`.
    """
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """
    Retrieves the full list of products in the inventory.
    
    Used by the Admin Dashboard to display stock levels and expiry dates.
    
    Args:
        db (Session): Database session.
        
    Returns:
        List[ProductResponse]: List of all products.
    """
    products = db.query(models.Product).all()
    return products

@app.get("/api/product/{barcode}", response_model=schemas.ProductResponse)
def get_product(barcode: str, db: Session = Depends(get_db)):
    """
    Looks up a single product by its barcode.
    
    Simulates the scanning action at the POS.
    
    Args:
        barcode (str): The scanned barcode.
        db (Session): Database session.
        
    Returns:
        ProductResponse: Product details if found.
        
    Raises:
        HTTPException(404): If the product is not found.
    """
    product = db.query(models.Product).filter(models.Product.barcode == barcode).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/checkout", response_model=schemas.TransactionResponse)
def checkout(request: schemas.CheckoutRequest, db: Session = Depends(get_db)):
    """
    Processes a checkout transaction.
    
    Core Logic:
    1. Validates the participant ID.
    2. Iterates through items, checking stock availability.
    3. Calculates total price.
    4. Decrements stock for each item (Critical for inventory tracking).
    5. Records the transaction and transaction items in the database.
    
    Args:
        request (CheckoutRequest): The checkout payload containing participant ID and items.
        db (Session): Database session.
        
    Returns:
        TransactionResponse: The created transaction ID and total amount.
        
    Raises:
        HTTPException(404): If participant or product is not found.
        HTTPException(400): If there is insufficient stock.
    """
    # Logic Step 1: Find Participant
    participant = db.query(models.Participant).filter(models.Participant.external_id == request.participant_external_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    total_amount = 0.0
    transaction_items = []
    
    # Logic Step 2: Loop through items and validate
    for item in request.items:
        product = db.query(models.Product).filter(models.Product.barcode == item.barcode).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with barcode {item.barcode} not found")
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        # Logic Step 3: Calculate price and prepare transaction item
        item_total = product.price * item.quantity
        total_amount += item_total
        
        # Decrement stock (Critical)
        product.stock_quantity -= item.quantity
        
        transaction_item = models.TransactionItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        transaction_items.append(transaction_item)

    # Create Transaction
    transaction = models.Transaction(
        participant_id=participant.id,
        total_amount=total_amount
    )
    db.add(transaction)
    db.commit() # Commit to get transaction ID
    db.refresh(transaction)

    # Link items to transaction
    for ti in transaction_items:
        ti.transaction_id = transaction.id
        db.add(ti)
    
    db.commit()
    
    return {"transaction_id": transaction.id, "total_amount": total_amount, "status": "success"}

@app.post("/api/external/camera")
def external_camera_event(payload: Dict[str, Any]):
    """
    Receives mock events from an external camera system.
    
    Used for data fusion research (e.g., correlating gaze/staring with purchases).
    
    Args:
        payload (Dict[str, Any]): Arbitrary JSON payload from the camera.
        
    Returns:
        dict: Status acknowledgment.
    """
    # Logging is acceptable for this mock interface
    # print(f"Received camera event: {payload}") 
    return {"status": "received"}

@app.get("/api/export/csv")
def export_csv(db: Session = Depends(get_db)):
    """
    Exports all transaction data as a CSV file for research analysis.
    
    Joins TransactionItem, Transaction, Product, and Participant tables to produce
    a flat dataset containing who bought what, when, and for how much.
    
    Args:
        db (Session): Database session.
        
    Returns:
        StreamingResponse: A downloadable CSV file named 'research_data.csv'.
    """
    # Query all transaction items joined with relevant tables
    results = db.query(
        models.TransactionItem,
        models.Transaction,
        models.Product,
        models.Participant
    ).join(
        models.Transaction, models.TransactionItem.transaction_id == models.Transaction.id
    ).join(
        models.Product, models.TransactionItem.product_id == models.Product.id
    ).join(
        models.Participant, models.Transaction.participant_id == models.Participant.id
    ).all()

    data = []
    for item, transaction, product, participant in results:
        data.append({
            "transaction_id": transaction.id,
            "timestamp": transaction.timestamp,
            "participant_external_id": participant.external_id,
            "participant_group": participant.group_id,
            "product_name": product.name,
            "product_barcode": product.barcode,
            "quantity": item.quantity,
            "price_paid": item.price_at_purchase
        })

    df = pd.DataFrame(data)
    
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=research_data.csv"
    return response
