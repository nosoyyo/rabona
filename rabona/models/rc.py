import logging

from .base import RabonaModel

# init
logging.basicConfig(
    filename='log/competition.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaCompetition(RabonaModel):
    pass
