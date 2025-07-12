from thronin.lib.logger_setup import LoggerSetup

# Initialize the logger
logging = LoggerSetup()
logger = logging.get_logger()
log_queue = logging.get_log_queue()
