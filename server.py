#!/usr/bin/env python3

# Actual application server. Answers calls from clients, according to API.

import bottle

@bottle.route('/')
def index():
    return 'True'

def run_server():
    bottle.run(host='127.0.0.1', port=8000)

if __name__ == '__main__':
    run_server()
