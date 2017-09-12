# Handler for uuid payloads.

import re
import uuid

from tradecraft import log

logger = log.logger.getChild('payload')

# Returns True if it's a uuid. Returns False otherwise.
def validate(payload):
    # Since I use only the entropic parts of the uuid, it's 32 hex chars.
    payload = payload.lower()
    if re.match(r'^[a-f0-9]{32}$', payload):
        logger.debug('Valid UUID: {}'.format(payload))
        return True
    logger.debug('Invalid UUID: {}'.format(payload))
    return False



