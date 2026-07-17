# main.py
#############################################
#dashboard thing
from database import Product
from pydantic import BaseModel
from typing import Optional

# This tells FastAPI exactly what data to expect from your Admin Dashboard
class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: int
    description: Optional[str] = None
    specs_html: Optional[str] = None
    protocol_html: Optional[str] = None
    support_html: Optional[str] = None
    download_link: Optional[str] = None
#############################################



from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# This physically loads the hidden file into Python's memory
load_dotenv() 

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SELLER_EMAIL = os.getenv("SELLER_ADDRESS")

# This creates our FastAPI application
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
# FIXED: Renamed from CartItem to Item so it matches the list below
class Item(BaseModel):
    id: int
    quantity: int

class QuoteSubmit(BaseModel):
    email: str
    company: str | None = None  # Catches the company name
    items: list[Item]

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "The Quote API is running!"}

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(database.Category).all()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(database.Product).all()
@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Create a new database row using the data from the dashboard
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully!", "product_id": new_product.id}

# --- EMAIL FUNCTION ---
def send_quote_email(buyer_email: str, quote_id: int, items_text: str, company: str):
    # FIXED: Re-added the message setup code
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = buyer_email
    msg['Subject'] = f"Quote Request Confirmation #{quote_id}"
    
    # Handle cases where they leave the company blank
    company_display = company if company else "No Company Provided"

    body = f"""Hello!
    
We have received a quote request (Order #{quote_id}) for {company_display}. 

Here is what was requested:
{items_text}

Our team will review these items and get back to you shortly.
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send to the buyer
        server.send_message(msg)
        
        # Swap the headers and send to the seller (store owner)
        msg.replace_header('To', SELLER_EMAIL)
        msg.replace_header('Subject', f"NEW LEAD: Quote #{quote_id} from {company_display}")
        server.send_message(msg)
        
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- QUOTE SUBMISSION ---
@app.post("/quotes")
def create_quote(quote: QuoteSubmit, db: Session = Depends(get_db)):
    # Save the company to SQLite
    new_quote = database.QuoteRequest(buyer_email=quote.email, company=quote.company)
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
    
    # Pass the company into the email function
    send_quote_email(quote.email, new_quote.id, email_items_text, quote.company)
    
    return {"message": "Quote received successfully!", "quote_id": new_quote.id}