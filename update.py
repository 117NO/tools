#!/usr/bin/python
# -*- coding: utf-8 -*-
import types
import MySQLdb
from sqlalchemy import Column, String, Integer,DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from table import *

#数据库配置 
SrcDB   = {"host":"127.0.0.1", "port":3306, "user":"root", "passwd":"", "dbname":"wordpress", "charset":"utf8"}
DstDB   = {"host":"127.0.0.1", "port":3306, "user":"root", "passwd":"", "dbname":"test", "charset":"utf8"}

# 1. 将需要修改的表定义为一个类
# 2. 将类名放入TableClasses列表中 
TableClasses = [post,user]
#本地的表的基本信息 Tables[tablename] = TableInfo
Tables = {}  



class TableInfo:
    _name=''
    _columns=''
    _maxJSID=0


def init_tables(DbConf):
    global Tables
    try:
        svrdb = MySQLdb.connect(host=DbConf['host'], port=DbConf['port'], user=DbConf['user'], passwd=DbConf['passwd'], 
                db=DbConf['dbname'], charset=DbConf['charset'])
    except MySQLdb.Error,e:
        print("connect to db failed! error %d: %s" % (e.args[0], e.args[1]))
    cursor = svrdb.cursor()
    try:
        cursor.execute("show tables")
    except MySQLdb.Error,e:
        print ("Get tables error! error %d: %s" % (e.args[0], e.args[1]))
        return
    tables  = cursor.fetchall()
    for row in tables:
        table = str(row[0])
        if table[:3]=="tmp":
            continue
        Info  = TableInfo()
        Info._name = table
        try:
            cursor.execute("select max(JSID) from %s" % table)
            result = cursor.fetchone() 
            if len(result)>0 and result[0] != None:
                Info._maxJSID = int(result[0])
                print "init table: %s %ld" % (table, Info._maxJSID)
        except MySQLdb.Error,e:
            print ("Get max(JSID) from %s  ERROR!  %d: %s" % (table, e.args[0], e.args[1]))
            continue
        
        try:
            cursor.execute("desc %s" % table) 
            desc = ""
            columns = cursor.fetchall()
            for column in columns:
                desc += str(column[0])
                desc += str(",")
            Info._columns = desc[:-1]
        except MySQLdb.Error,e:
            print (" desc %s fail! error %d: %s" % (table, e.args[0], e.args[1]))
            return ""
        Tables[table] = Info
    cursor.close()


def obj2dict(obj):
    dt = {}
    for name in dir(obj):
        value = getattr(obj, name) 
        if False== name.startswith('_') and not callable(value) and name!='metadata':
            dt[name] = value
    return dt


if __name__=="__main__":
    
    init_tables(DstDB)


    SrcEngine = create_engine('mysql://%s:%s@%s:%d/%s?charset=%s' % \
            (SrcDB['user'], SrcDB['passwd'],SrcDB['host'], SrcDB['port'],SrcDB['dbname'],SrcDB['charset']), echo=False)
    SrcDBsession = sessionmaker(bind=SrcEngine)
    SrcSession = SrcDBsession()

    DstEngine = create_engine('mysql://%s:%s@%s:%d/%s?charset=%s' % \
            (DstDB['user'], DstDB['passwd'],DstDB['host'], DstDB['port'],DstDB['dbname'],DstDB['charset']),  echo=False)
    DstDBsession = sessionmaker(bind=DstEngine)
    DstSession = DstDBsession()


    for table in TableClasses:
        print 'updating table %s' % table.__tablename__
        condition = table.JSID>Tables[table.__tablename__]._maxJSID
        UpdatedRows = SrcSession.query(table).filter(condition).all()
        SrcSession.close()
        for row in UpdatedRows:
            RowMatch=DstSession.query(table).filter(table.id==row.id)
            if 1==RowMatch.count():
                try:
                    dic = obj2dict(row)
                    RowMatch.update(dic)
                except:
                    print 'update fail'
            else:
                assert 0==RowMatch.count()
                try:
                    DstSession.merge(row)
                    DstSession.flush()
                except:
                    print 'insert fail'
            DstSession.commit()
    DstSession.close()



