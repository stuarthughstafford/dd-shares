from ddtrace import tracer, patch_all; patch_all(logging=True)
from flask import Flask
import logging
import json_log_formatter

app = Flask(__name__)

# Set the logging so the traces and logs are correlated
formatter = json_log_formatter.JSONFormatter()
json_handler = logging.StreamHandler()
json_handler.setFormatter(formatter)
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logger = logging.getLogger('my_json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

@app.route('/')
def index():
	#logger.info('test', extra={'test_json': 'hello world'})
	#logger.info({"special": "value", "run": 12})
    return 'hello world!!'

@app.route('/test_endpoint')
def test_endpoint():
    #logging.info("Test logging")
    logger.info({"endpoint": "test_endpoint", "check": "See if this message is correlated in Datadog"})
    return 'hello Test logging!!'
	
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
