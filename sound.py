import logging
import os

logger = logging.getLogger()


class LocalSound:

    def play(self, file):
        self.stop()
        logger.info('playing file: %s', file)
        os.system('(play -q %s > /dev/null) &' % file)

    def stop(self):
        logger.info('stop playing')
        os.system('pkill -x play')
