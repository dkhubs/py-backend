from kombu import Exchange, Queue

from config import load_config

celeryInfo = load_config()['Celery']

broker_url          = celeryInfo['Broker']
result_backend      = celeryInfo['ResultBackend']

result_expires      = celeryInfo['ResultExpires']
task_serializer     = 'json'
result_serializer   = 'json'
accept_content      = ['json']
timezone            = celeryInfo['Timezone']
enable_utc          = celeryInfo['EnableUTC']

# 优先级队列设置
# always_eager = True
task_acks_late = celeryInfo['TaskAcksLate']
worker_prefetch_multiplier = celeryInfo['WorkerPrefetchMultiplier']

task_queues = {
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('msg', Exchange('msg'), routing_key='msg', queue_arguments={'x-max-priority': 5})
}

task_default_exchange = celeryInfo['TaskDefaultExchange']
task_default_routing_key = celeryInfo['TaskDefaultRoutingKey']
