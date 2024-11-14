import os
from fastapi import FastAPI
from datetime import datetime, timezone, timedelta
from routers import stt, data
from dotenv import load_dotenv
from utils.logger import logger
from services.transcription import TranscriptionService
from services.vad import get_vad_service

## Setup OS/DIR Path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

## Load environment variables
load_dotenv(override=True)

# Initialize FastAPI
app = FastAPI()

async def startup():
    """
    Initialize services on application startup
    """
    logger.info("Starting application initialization...")
    
    try:
        # Initialize VAD service
        get_vad_service()

        # Initialize transcription service
        service = TranscriptionService(api_key=os.getenv("HF_TOKEN", ""))
        warm_up_success = await service.warm_up()
        if warm_up_success:
            logger.info("Model warm-up completed successfully")
        else:
            logger.warning("Model warm-up was not successful, but application will continue")
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        logger.warning("Application will start, but performance may be affected")
    
    logger.info("Application startup completed")

async def shutdown():
    """
    Cleanup on application shutdown
    """
    logger.info("Application shutdown initiated")
    try:
        # Cleanup VAD service
        vad_service = get_vad_service()
        vad_service.cleanup()
        logger.info("VAD service cleaned up successfully")
    except Exception as e:
        logger.error(f"Error cleaning up VAD service: {str(e)}")

# Add event handlers
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

@app.get("/health")
async def health_check():
    try:
        gmt_plus_8 = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))    
        return {
            "status": "ok",
            "timestamp": gmt_plus_8
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise
    
# Add routers
app.include_router(stt.router)
app.include_router(data.router)