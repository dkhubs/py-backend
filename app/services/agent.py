

import logging, threading, time

from loguru import logger

class AgentChecker(threading.Thread):
    def __init__(self):
        logger.log(logging.INFO, '[Agent Checker] 初始化 Agent Checker 实例 ...')
        super(AgentChecker, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        logger.log(logging.INFO, '[Agent Checker] 退出 Agent Checker 线程 ...')
        self._stop_event.set()

    def run(self):
        logger.log(logging.INFO, '[Agent Checker] 启动检查Agent上报状态线程...')
        while not self._stop_event.is_set():
            logger.log(logging.INFO, '[Agent Checker] *** Todo 检查Agent上报状态 ***')

            time.sleep(3)