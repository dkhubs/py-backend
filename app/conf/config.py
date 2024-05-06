
import sys, os, logging, yaml

from loguru import logger
from typing import cast
from types import FrameType

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def config_logger(LOGGING_LEVEL):
    logging.getLogger().handlers = [InterceptHandler(level=LOGGING_LEVEL)]
    for logger_name in ['uvicorn.asgi', 'uvicorn.access']:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
    logger.configure(handlers=[{'sink': sys.stderr, 'level': LOGGING_LEVEL}])

def load_config(filename = 'config.yaml'):
    if not os.path.exists(filename):
        sys.exit(f'Not find {filename} file')
    
    confInfo = None
    LOGGING_LEVEL = logging.INFO
    with open(filename, 'r') as file:
        confInfo = yaml.safe_load(file)
        
        # 根据日志级别, 配置 Logger
        if confInfo.get('DEBUG'):
            LOGGING_LEVEL = logging.DEBUG

        config_logger(LOGGING_LEVEL)
    
    return confInfo