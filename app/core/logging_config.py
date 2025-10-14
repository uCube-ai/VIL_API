import os
import logging
from .config import settings

def setup_transaction_logger():
    """
    Sets up the base logger for transaction logs.
    Handlers for specific files will be added and removed dynamically per request.
    """
    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    
    logger = logging.getLogger("transaction_logger")
    
    logger.setLevel(logging.INFO)
    
    # Set propagate to False to prevent logs from being passed to the root logger.
    # This stops messages from appearing in the console twice.
    logger.propagate = False