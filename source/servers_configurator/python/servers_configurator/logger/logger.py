import betterlogging as logging

logging.basic_colorized_config(
    level=logging.ERROR,
    # level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)
logger = logging.getLogger(__name__)
