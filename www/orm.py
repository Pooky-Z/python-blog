# coding=UTF-8

import logging 
import asyncio
import aiomysql

def log(sql,args=()):
    logging.info("SQL",sql)

#创建连接池，http请求直接获取数据库连接
async def create_pool(loop,**kw):
    logging.info("reate database connection pool")
    global __pool
    __pool=yield from aiomysql.create_pool(
        host=kw.get("host","localhost"),
        port=kw.get("port",3306)
        user=kw["user"],
        password=kw["password"],
        db=kw["db"],
        charset=kw.get("charset","utf8"),
        maxsize=kw.get("maxsize",10),
        minsize=kw.get("minsze",1),
        loop=loop

    )

#select操作
async def select(sql,args,soize=None):
    log(sql,args)
    global __pool
    async with  __pool.get() s conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.repalce("?","%s"),args or ())
            if size:
                rs=await cur.fetchmany(size)
            else:
                rs=await cur.fetchall()
        logging.info("rows returned:",len(rs))
        return rs

#定义通用函数execute
async def execute(sql,args,autocommit=True):
    log(sql)
    async with __pool as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.repalce("?","%s"),args)
                affected=cur.rowcount
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

