import logging
import os

def setup_logging():
    """Configure logging to write to a file."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{log_dir}/trading_bot.log"),
            logging.StreamHandler() # Also print to console
        ]
    )
    return logging.getLogger(__name__)