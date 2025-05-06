from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.routes import qa

app = FastAPI(
    title="LLM Q&A API",
    description="A FastAPI backend for an LLM-powered Q&A application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(qa.router, prefix="/api", tags=["qa"])

# Redirect root to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    from decouple import config
    
    host = config("HOST", default="0.0.0.0")
    port = config("PORT", cast=int, default=8000)
    
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
