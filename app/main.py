# -- encoding:utf-8 --
import asyncio, logging, time, websockets

from loguru import logger
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from uvicorn import Config, Server

from conf.config import load_config
from conf.middleware import AuthMiddleware
from routers.api import router

from services import agent

# 加载配置
CONFIG_INFO = load_config()

# 实例化 & 启动 FastAPI
svcConfig = CONFIG_INFO['Server']
app = FastAPI(title=svcConfig.get('Name'), version=svcConfig.get('Version'))
app.add_middleware(AuthMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(router, prefix=svcConfig.get('ApiPrefix'))

# 
async def websockets_handler(websocket, path):
    async for msg in websocket:
        logger.log(logging.INFO, '服务端接收的消息:{}'.format(msg))
        
        respMsg = 'Response Time: {}'.format(time.time())
        await websocket.send(respMsg)

# 
wsConfig = CONFIG_INFO['WebSocket']
wsServer = websockets.serve(websockets_handler, wsConfig.get('Host'), wsConfig.get('Port'))
appServer = Server(Config(app, host=svcConfig.get('Host'), port=svcConfig.get('Port'), reload=True))

async def start_serve():
    await asyncio.gather(wsServer, appServer.serve())

# 启动AgentChecker线程
agentThread = agent.AgentChecker()
agentThread.start()

try:
    asyncio.get_event_loop().run_until_complete(start_serve())
finally:
    # 退出线程
    agentThread.stop()
    agentThread.join()
    