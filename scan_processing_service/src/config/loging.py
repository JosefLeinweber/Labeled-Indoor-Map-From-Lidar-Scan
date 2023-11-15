import loguru
import sys


def setup_logging() -> None:
    loguru.logger.remove(handler_id=None)
    dev_log_format = "<level>{level: <8}|</level><cyan>{function}</cyan>:<cyan>{line}</cyan> \t:<g><level>{message}</level></g>"
    loguru.logger.add(sys.stderr, format=dev_log_format)
    loguru.logger.success("Logging setup completed!")
