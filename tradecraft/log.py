# Single invocation of logging utility for other modules to ingest.

import logging

formatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s:%(message)s', 
    datefmt='%Y-%m-%dT%H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=logging.DEBUG)
