import logging

logger = logging.getLogger('jobs')

from config import config
from .bean import Bean
from .bean_app import BeanApp
from .red_packet import RedPacket
from .sign_jr import SignJR
from .daka_app import DakaApp
from .double_sign import DoubleSign
from .data_station import DataStation
from .jr_fanpai import fanpai
from .jr_promote_amount import baitiao

__all__ = ['jobs_all', 'logger']

jobs_mobile = [DakaApp, BeanApp, DataStation]
jobs_web = [Bean, SignJR, RedPacket, fanpai, baitiao]
jobs_all = jobs_mobile + jobs_web + [DoubleSign]


def set_logger():
    # 设置基本属性
    logger.propagate = False
    logger.setLevel(logging.INFO)

    # 设置handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(config.log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


set_logger()
