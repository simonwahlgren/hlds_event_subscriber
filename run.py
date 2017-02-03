#!/usr/bin/env python3
import dill
import logging
import os
import time

from redis import StrictRedis

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
logger.addHandler(console)

from gpio import RPiGPIO
gpio = RPiGPIO()
CT_LIGHT = 26
TS_LIGHT = 19
PARTY = 13

redis = StrictRedis(os.getenv('REDIS_HOST', 'localhost'))
redis_pubsub = redis.pubsub(ignore_subscribe_messages=True)
redis_pubsub.subscribe('hlds_events')

ct_score, ts_score = None, None


def hlds_event_machine(event, groups):
    global ct_score, ts_score

    if event == 'team_cts_win_round':
        gpio.on(CT_LIGHT)
    elif event == 'team_ts_win_round':
        gpio.on(TS_LIGHT)
    elif event == 'round_start':
        gpio.off(CT_LIGHT)
        gpio.off(TS_LIGHT)
        gpio.off(PARTY)
    elif event == 'team_cts_win_game':
        score, _ = groups
        ct_score = int(score.decode('utf-8'))
    elif event == 'team_ts_win_game':
        score, _ = groups
        ts_score = int(score.decode('utf-8'))

    if ct_score is not None and ts_score is not None:
        if ct_score > ts_score:
            gpio.on(CT_LIGHT)
            logger.info("Team CT won game with %d - %d" % (ct_score, ts_score))
        else:
            gpio.on(TS_LIGHT)
            logger.info("Team TERRORIST won game with %d - %d" % (ts_score, ct_score))
        gpio.on(PARTY)
        ct_score, ts_score = None, None


if __name__ == '__main__':
    logger.info("Starting HLDS event subscriber")
    while True:
        message = redis_pubsub.get_message()
        if message:
            data = dill.loads(message['data'])
            event, groups = data
            logger.info("Received event %s with data %s" % (event, groups))
            hlds_event_machine(event, groups)

        time.sleep(0.1)
