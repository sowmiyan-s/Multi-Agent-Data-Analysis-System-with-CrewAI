import sys
import os
from loguru import logger
from config.app_config import settings

def setup_logger():
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stderr, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO"
    )
    
    # File handler
    log_file = os.path.join(settings.LOG_DIR, "app.log")
    logger.add(
        log_file,
        rotation="10 MB",
        retention="1 week",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )
    
    return logger

# Initialize logger
app_logger = setup_logger()
