import os
import logging
from contextlib import contextmanager
from datetime import datetime, timezone
from .config import settings

logger = logging.getLogger("transaction_logger")
logger.setLevel(logging.INFO)
logger.propagate = False

def setup_transaction_logger():
    """
    Ensures the logs directory exists.
    Called on app startup.
    """
    os.makedirs(settings.LOGS_DIR, exist_ok=True)

@contextmanager
def transaction_logging(table_name: str, operation: str):
    """
    Context manager that dynamically attaches a FileHandler to the transaction_logger
    for the duration of a request, and guarantees cleanup.
    """
    # 1. Setup Filename and Path
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    log_filename = f"{operation}_{table_name}_{timestamp}.txt"
    log_filepath = os.path.join(settings.LOGS_DIR, log_filename)

    # 2. Configure Handler
    file_handler = logging.FileHandler(log_filepath)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    
    # 3. Attach Handler
    logger.addHandler(file_handler)
    
    try:
        # 4. Log the Start Header automatically
        logger.info("=" * 50)
        logger.info(f"STARTING {operation.upper()} FOR '{table_name}'")
        logger.info(f"Log file: {log_filename}")
        logger.info("=" * 50)
        
        yield log_filename
        
    finally:
        # 5. Guaranteed Cleanup (Detach and Close)
        logger.info("=" * 50)
        logger.info("END OF TRANSACTION")
        logger.info("=" * 50)
        
        logger.removeHandler(file_handler)
        file_handler.close()
