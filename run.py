from hbc import app, views
from hbc import debug_logging, online_logging

if __name__ == '__main__':
    debug_logging('log\error.log')
    app.run(port=8098, threaded=True)
