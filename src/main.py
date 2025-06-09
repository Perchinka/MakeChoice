import os
import uvicorn
from src.api.app import app
from src.config import settings

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = settings.ENV == "development"
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
    )
