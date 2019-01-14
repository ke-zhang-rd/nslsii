import logging
import requests


class ElasticHandler(logging.Handler):
    '''
    Logging handler that submits data to Elastic

    Parameters
    ----------
    url: string
        url to Elastic server

    level: Logging Levels, optional
        Handler logging level
    '''
    def __init__(self, url, level=logging.INFO):
        self.url = url
        self.level = level
        super().__init__(self.level)

    def emit(self, record):
        '''
        method is used to send the message to its destination and
        logging for debug
        '''
        # Extract useful info from the record and put them into a dict.
        try:
            record_dict = {'name': record.name,
                           'levelno': record.levelno,
                           'pathname': record.pathname,
                           'lineno': record.lineno,
                           'msg': record.msg,
                           'args': record.args,
                           'exc_info': record.exc_info,
                           'sinfo': record.sinfo}
            response = requests.post(self.url, json=record_dict)
            response.raise_for_status()
        except Exception:
            self.handleError(record)


bluesky_logger = logging.getLogger('bluesky')
carproto_logger = logging.getLogger('carproto')
ophyd_logger = logging.getLogger('ophyd')

elastic_hdr = ElasticHandler('http://elasticsearch.cs.nsls2.local/test/_doc/1')

bluesky_logger.addHandler(elastic_hdr)
carproto_logger.addHandler(elastic_hdr)
ophyd_logger.addHandler(elastic_hdr)