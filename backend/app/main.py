from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import contact_routes, contact_list_routes, auto_dialer_routes, user_routes
from .config import settings
from .database import engine
from .models import user, contact, contact_list, call_record

# Create database tables
user.Base.metadata.create_all(bind=engine)
contact.Base.metadata.create_all(bind=engine)
contact_list.Base.metadata.create_all(bind=engine)
call_record.Base.metadata.create_all(bind=engine)

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