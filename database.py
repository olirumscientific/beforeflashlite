from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# 1. Setup SQLite Database URL (this creates a file named olirum.db in your project folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# 2. Create the SQLAlchemy Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class (each instance is a database session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class for our models to inherit from
Base = declarative_base()


# --- DATABASE MODELS (TABLES) ---

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    # Relationship: A category can have many products
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # --- Technical & Marketing Columns ---
    # These store the data that JavaScript will pull for the Single Product View
    description = Column(String, nullable=True)
    protocol_html = Column(String, nullable=True)
    specs_html = Column(String, nullable=True)
    support_html = Column(String, nullable=True)
    download_link = Column(String, nullable=True)
    is_archived = Column(Boolean, default=False)
    
    # Relationship: A product belongs to one category
    category = relationship("Category", back_populates="products")

# 4. Define the QuoteRequest Table
class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    company = Column(String, nullable=True)
    city = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

    # This links the quote request to the specific items ordered
    items = relationship("QuoteItem", back_populates="quote")

# 5. Define the QuoteItem Table (The Junction!)
class QuoteItem(Base):
    __tablename__ = "quote_items"

    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("quote_requests.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    # This is the line that completes the handshake!
    quote = relationship("QuoteRequest", back_populates="items")

# Create all tables in the database
Base.metadata.create_all(bind=engine)