import logging
import sys

from core.config import settings


formatter = logging.Formatter(
    fmt="[%(levelname)-8s %(asctime)s.%(msecs)s]"
    " %(module)-20s:%(lineno)4s - %(message)s",
    datefmt=r"%Y-%M-%d %H:%M:%S",
)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)


logger.addHandler(handler)
logger.setLevel(settings.log_level)
