from .database import engine, Base
from .models import User, Contact, ContactList, contact_list_association
from .routes import user_routes, contact_routes, contact_list_routes, auto_dialer_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from sqlalchemy import inspect

def create_tables_if_not_exist():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    for table in Base.metadata.tables.values():
        if table.name not in existing_tables:
            table.create(engine)

# Call the function to create tables if they don't exist
create_tables_if_not_exist()

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(contact_routes.router, prefix="/api/contacts", tags=["contacts"])
app.include_router(contact_list_routes.router, prefix="/api/contact-lists", tags=["contact lists"])
app.include_router(auto_dialer_routes.router, prefix="/api/auto-dialer", tags=["auto dialer"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Auto Dialer API"}