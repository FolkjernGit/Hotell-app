from typing import Annotated

from sqlalchemy import  String, SmallInteger, Integer
from sqlalchemy.orm import mapped_column


str_255 = Annotated[str, mapped_column(String(255))]
pkey = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
s_int = Annotated[int, mapped_column(SmallInteger)]

