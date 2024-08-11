from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import contact_routes, contact_list_routes, auto_dialer_routes
from app.config import settings

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
app.include_router(contact_routes.router, prefix="/api/contacts", tags=["contacts"])
app.include_router(contact_list_routes.router, prefix="/api/contact-lists", tags=["contact lists"])
app.include_router(auto_dialer_routes.router, prefix="/api/auto-dialer", tags=["auto dialer"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Auto Dialer API"}