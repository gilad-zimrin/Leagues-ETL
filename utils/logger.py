import logging
import json
import sys
import traceback
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """
    Format logs as JSON with common best-practice fields.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info
            log_record["exception"] = f"""
                "type": {str(exc_type.__name__)},
                "message": {str(exc_value)},
                "stacktrace": {"".join(traceback.format_exception(exc_type, exc_value, exc_tb))}
            """

        return json.dumps(log_record, ensure_ascii=False)

def get_logger(name: str = "app_logger") -> logging.Logger:
    """
    Return a logger instance configured for JSON output.
    """
    new_logger = logging.getLogger(name)
    if not new_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        new_logger.addHandler(handler)
        new_logger.setLevel(logging.INFO)
        new_logger.propagate = False
    return new_logger

logger = get_logger()
