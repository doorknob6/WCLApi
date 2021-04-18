from dotenv import load_dotenv

load_dotenv("test/.env")

import logging

api_logger = logging.getLogger("WCLApi")
api_logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
fmt = logging.Formatter(
    "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(fmt)
api_logger.addHandler(stream_handler)

import sys
from os import getenv
from os.path import join, dirname

sys.path.append(join(dirname(__file__), ".."))

from WCLApi import WCLApi


def test_api_init():
    return WCLApi(getenv("WCL_API_KEY"))


def test_reports():
    api = test_api_init()
    guild_name = "Nerf Inc"
    server = "nethergarde-keep"
    region = "EU"
    start = 1596578400000
    end = 1606950000000
    cont = api.get_guild_reports(
        server=server,
        server_region=region,
        guild_name=guild_name,
        start_time=start,
        end_time=end,
    )
