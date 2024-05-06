from datetime import datetime
import logging, threading, redis

from loguru import logger

from conf.config import load_config

class RedisCli:
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(RedisCli, '_instance'):
            with RedisCli._instance_lock:
                if not hasattr(RedisCli, '_instance'):
                    RedisCli._instance = RedisCli(*args, **kwargs)
        return RedisCli._instance

    def __init__(self) -> None:
        logger.log(logging.INFO, '*** 初始化 RedisCli 实例 *** {} '.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
        
        redisConf = load_config()['Redis']
        self.redis_cli = redis.StrictRedis(host=redisConf['Host'], port=int(redisConf['Port']), db=int(redisConf['DB']))
