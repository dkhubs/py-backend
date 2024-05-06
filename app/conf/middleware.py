import jwt

from datetime import datetime
from loguru import logger
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from conf.config import load_config
from services import cache
from utils.tools import gen_random_code

redisClient = cache.RedisCli.instance().redis_cli

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        requestId = request.headers.get('X-Request-ID')
        if not requestId:
            # 随机生成一个字符串
            requestId = gen_random_code()
            # return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'code':-1, 'msg': 'Miss Param `X-Request-ID` in Request Header: {}'.format(request.headers)})

        # if access url in white list call_next
        access_url = request.scope['path']
        if access_url in ['/docs', '/openapi.json', '/api/devops/task/health', '/api/devops/task/reload', '/api/devops/auth/access_check', '/api/devops/task/hooks/gitlab/ci_events']:
            return await call_next(request)
        
        # check X-Token
        xtoken = request.headers.get('X-Token')
        if not xtoken:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'code':401, 'msg': 'Miss Param `X-Token` in Request Header'})

        # Check X-Token && Set User Access Auth
        try:
            # 判断X-Token是否已作废
            revkToken = redisClient.hget('SREService:RevokedToken', xtoken)
            if revkToken:
                raise jwt.ExpiredSignatureError('Token 已作废')
            
            uinfo = jwt.decode(xtoken, load_config()['SecretKey'], 'HS256')
            
            username = uinfo.get('name')
            request.scope['user'] = username
            
            expTime = uinfo.get('exp')
            if int(datetime.now().timestamp()) < expTime:
                return await call_next(request)
            else:
                redisClient.hdel('SREService:Token', username)
                raise jwt.ExpiredSignatureError('Token 已过期')
        
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'code': 400, 'msg': '{}'.format(e)})