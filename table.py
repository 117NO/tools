#!/usr/bin/python

from sqlalchemy import Column, String, Integer,DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class post(Base):
    __tablename__   =   'wp_posts'
    id              =   Column(Integer, primary_key=True)
    post_title      =   Column(String)
    post_content    =   Column(String)
    post_date       =   Column(DateTime)
    post_author    =   Column(String)
    JSID         =   Column(Integer)


class user(Base):
    __tablename__   =   'wp_users'
    id              =   Column(Integer, primary_key=True)
    user_nicename   =   Column(String)
    user_email      =   Column(String)
    user_url        =   Column(String)
    user_status     =   Column(Integer)
    JSID         =   Column(Integer)

