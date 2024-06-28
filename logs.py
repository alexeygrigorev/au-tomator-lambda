import sys
import json

import logging
from datetime import datetime, UTC


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.now(UTC).isoformat() + 'Z',
            'level': record.levelname,
            'message': record.getMessage(),
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

formatter = JSONFormatter()

ch.setFormatter(formatter)
logger.addHandler(ch)
