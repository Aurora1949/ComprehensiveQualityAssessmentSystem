import mimetypes
import re
import hashlib

import aiofile
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import crud


def is_uid_valid(uid: str) -> bool:
    return bool(re.match("^[12][0-9]{9}$", uid))


async def is_user_exists(uid: str, db: AsyncSession):
    return bool(await crud.get_user_by_account(db, uid))


def hashed_string(string: str) -> str:
    hasher = hashlib.sha256()
    hasher.update(string.encode('utf-8'))
    return hasher.hexdigest()


async def write_file_to_disk(filename: str, data: UploadFile):
    await data.seek(0)
    async with aiofile.async_open(filename, 'wb') as f:
        await f.write(await data.read())


async def get_file_md5(data: UploadFile) -> str:
    hash_md5 = hashlib.md5()
    hash_md5.update(await data.read())
    return hash_md5.hexdigest()


async def read_file(file_path: str):
    async with aiofile.async_open(file_path, 'rb') as f:
        while True:
            chunk = await f.read(1024*1024)  # 读取每次1MB的数据
            if not chunk:
                break
            yield chunk


def get_media_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"
