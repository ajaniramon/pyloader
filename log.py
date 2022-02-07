import logging


def configure_logging():
    logging.basicConfig(filename="pyloader.log", filemode="w", format="'%(asctime)s - %(message)s'", level="DEBUG")


def log_debug(msg):
    print(msg)
    logging.debug(msg)


def log(msg):
    print(msg)
    logging.info(msg)
