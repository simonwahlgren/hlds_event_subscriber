#!/usr/bin/env python3.6
import dill
import logging
import os
import time

from redis import StrictRedis

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
logger.addHandler(console)

redis = StrictRedis(os.getenv('REDIS_HOST', 'localhost'))
redis_pubsub = redis.pubsub(ignore_subscribe_messages=True)
redis_pubsub.subscribe('hlds_events')

logger.info("Starting HLDS event subscriber")

ct_score, ts_score = None, None


def hlds_event_machine(event, groups):
    global ct_score, ts_score

    if event == 'team_cts_win_game':
        score, _ = groups
        ct_score = int(score.decode('utf-8'))
        logger.info("Team CT scored %d" % ct_score)
    elif event == 'team_ts_win_game':
        score, _ = groups
        ts_score = int(score.decode('utf-8'))
        logger.info("Team TERRORIST scored %d" % ts_score)

    if ct_score is not None and ts_score is not None:
        if ct_score > ts_score:
            logger.info("Team CT won game with %d - %d" % (ct_score, ts_score))
        else:
            logger.info("Team TERRORIST won game with %d - %d" % (ts_score, ct_score))
        ct_score, ts_score = None, None


while True:
    message = redis_pubsub.get_message()
    if message:
        data = dill.loads(message['data'])
        event, groups = data
        logger.info(f"Received event {event} with data {groups}")
        hlds_event_machine(event, groups)

    time.sleep(0.1)
