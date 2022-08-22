#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 6:54 PM
# @File    : db.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
