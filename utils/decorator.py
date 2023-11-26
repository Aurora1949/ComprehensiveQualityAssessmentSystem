import logging
import os
from functools import wraps
from typing import Callable

from fastapi import HTTPException, Header

if not os.path.exists('./log'):
    os.makedirs('./log')

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s: %(message)s',
    level=logging.CRITICAL,
    filename='./log/fatal.log',
    filemode='a',
    datefmt='%Y-%m-%d %A %H:%M:%S'
)


def record_fatal_error(func: Callable, header: Header = None) -> Callable:
    """
    see https://blog.csdn.net/mutao1127877836/article/details/127285381
    :param header:
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except BaseException as e:
            logging.critical(f'at {func.__name__}() {str(e)}')
            raise HTTPException(status_code=500, detail="fatal error occurred, please see log.")

    return wrapper
