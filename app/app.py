from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

app = FastAPI(title="Sift Data ExtractionAPI", description="Extract structured data from pdfs and images", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #TODO: change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return { "message": "Sift Data Extraction API is running.", "docs": "/docs", "version": "1.0.0" }
   

@app.get("/health")
async def health_check():
    return { "status": "healthy"}