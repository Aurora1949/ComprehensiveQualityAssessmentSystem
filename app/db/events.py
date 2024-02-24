#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/01/31
#  Last Modified on 2024/01/31 05:59:21
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import aiosqlite
from fastapi import FastAPI
from loguru import logger

from app.core.settings.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to SQLite database... {}".format(settings.database_url))

    app.state.sqlite = await aiosqlite.connect(str(settings.database_url))

    logger.info("Connected established connection to SQLite database.")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to SQLite database...")

    await app.state.sqlite.close()

    logger.info("Connection closed.")
