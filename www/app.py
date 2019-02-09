#coding=UTF-8
import logging;logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web

def index(requst):
    return web.Response(body=b"<h1>hello,BLOG</h1>",content_type="text/html")

async def init(loop):
    #创建一个Web服务器实例
    app=web.Application(loop=loop)
    #注册URL
    app.router.add_route("GET","/",index)
    srv=await loop.create_server(app.make_handler(),"127.0.0.1",9004)
    logging.info('server started at http://127.0.0.1:9004...')
    print(type(srv))
    # return srv
loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
