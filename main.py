# main.py
#############################################
# dashboard thing
from database import Product
from pydantic import BaseModel
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: int
    description: Optional[str] = None
    specs_html: Optional[str] = None
    protocol_html: Optional[str] = None
    support_html: Optional[str] = None
    download_link: Optional[str] = None

# NEW: Model for editing products so we don't have to submit every field
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    specs_html: Optional[str] = None
    protocol_html: Optional[str] = None
    support_html: Optional[str] = None
    download_link: Optional[str] = None
    is_archived: Optional[bool] = None
#############################################
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv() 

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SELLER_EMAIL = os.getenv("SELLER_ADDRESS")

app = FastAPI()

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE DEPENDENCY ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- PYDANTIC MODELS ---
class Item(BaseModel):
    id: int
    quantity: int

class QuoteSubmit(BaseModel):
    name: str
    email: str
    company: str | None = None
    city: str
    pincode: str
    items: List[Item]

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "The Quote API is running!"}

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(database.Category).all()

# UPDATED: Only return active (non-archived) products for the main catalog
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(database.Product).filter(database.Product.is_archived == False).all()

# NEW: Return all products (including archived) for the Admin Dashboard
@app.get("/admin/products")
def get_admin_products(db: Session = Depends(get_db)):
    return db.query(database.Product).all()

@app.post("/products")
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    x_admin_token: str = Header(None)  # FastAPI looks for 'X-Admin-Token' in the request headers
):
    # 1. Verify the password
    correct_password = os.getenv("ADMIN_PASSWORD")
    if x_admin_token != correct_password:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin Password")
    
    # 2. If the password is correct, proceed with saving to the database
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully!", "product_id": new_product.id}

# UPDATED: Edit product using the new ProductUpdate model
@app.put("/products/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    # Find the existing product
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update only the fields that were provided (exclude_unset=True)
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}

# NEW: Archive product (Soft Delete)
@app.put("/products/{product_id}/archive")
def archive_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db_product.is_archived = True
    db.commit()
    return {"message": f"Product {product_id} archived successfully"}

# --- EMAIL FUNCTION ---
def send_quote_email(quote_id: int, quote: QuoteSubmit, items_text: str):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = quote.email
    msg['Subject'] = f"Quote Request Confirmation #{quote_id} - Olirum Scientific"
    
    company_display = quote.company if quote.company else "Independent Researcher"

    # Formatted email body containing all the new lead information
    body = f"""Hello {quote.name},
    
Thank you for reaching out to Olirum Scientific. We have received your quote request (Order #{quote_id}).

LEAD DETAILS:
Name: {quote.name}
Email: {quote.email}
Institution: {company_display}
Location: {quote.city}, {quote.pincode}

REQUESTED ITEMS:
{items_text}

Our technical sales team will review your requirements and get back to you shortly with pricing and shipping logistics.

Best regards,
The Olirum Scientific Team
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send confirmation to the buyer
        server.send_message(msg)
        
        # Swap headers and send lead alert to you (the seller)
        msg.replace_header('To', SELLER_EMAIL)
        msg.replace_header('Subject', f"NEW LEAD: Quote #{quote_id} from {quote.name} ({quote.city})")
        server.send_message(msg)
        
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- QUOTE SUBMISSION ---
@app.post("/quotes")
def create_quote(quote: QuoteSubmit, db: Session = Depends(get_db)):
    
    # CRITICAL: Make sure your database.py QuoteRequest model has these new columns!
    new_quote = database.QuoteRequest(
        buyer_name=quote.name,
        buyer_email=quote.email, 
        company=quote.company,
        city=quote.city,
        pincode=quote.pincode
    )
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)

    email_items_text = ""

    for item in quote.items:
        product = db.query(database.Product).filter(database.Product.id == item.id).first()
        product_name = product.name if product else "Unknown Product"

        quote_item = database.QuoteItem(
            quote_id=new_quote.id,
            product_id=item.id,
            quantity=item.quantity
        )
        db.add(quote_item)
        email_items_text += f"- {item.quantity}x {product_name}\n"
    
    db.commit()
    
    # Send the email with the full quote object
    send_quote_email(new_quote.id, quote, email_items_text)
    
    return {"message": "Quote received successfully!", "quote_id": new_quote.id}