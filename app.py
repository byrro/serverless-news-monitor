'''Demo of a Serverless News Articles Monitor Application using AWS Lambda'''
import json
import logging
from chalice import Chalice
from chalicelib import utils


app = Chalice(app_name='serverless-news-monitor')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)


@app.route('/', methods=['GET', 'POST'])
@app.route('/{action}', methods=['GET', 'POST'])
@app.route('/{action}/{param1}', methods=['GET', 'POST'])
@app.route('/{action}/{param1}/{param2}', methods=['GET', 'POST'])
def run(*args, **kwargs):
    # Log all incoming requests for monitoring and security purposes
    # Json format is easier to read on log applications, such as AWS CloudWatch
    # and Dashbird.io
    print('app.current_request:')
    print(json.dumps(app.current_request.to_dict()))

    try:
        request_handler = utils.request_handler_constructor(
            request=app.current_request.to_dict(),
            action=kwargs.get('action'),
            param1=kwargs.get('param1'),
            param2=kwargs.get('param2'),
        )

        response = request_handler.run()

        # Log all responses for monitoring and security purposes
        if response.error:
            print('response.error:')
            print(json.dumps(response.error))
            return response.error

        else:
            # Streamlined version of the payload for logging purposes
            streamlined_payload = utils.streamline_payload(
                payload=response.payload
            )

            print('reponse.payload:')
            print(json.dumps(streamlined_payload))

            return response.payload

    except TypeError as error:
        utils.log_exception(error=error)
        return {
            'status': 400,
            'error': str(error),
        }

    # Make sure uncaught errors are handled properly
    except Exception as error:
        utils.log_uncaught_exception(error=error)

        return {
            'status': 500,
            'error':
                'Heck, the Serverless Gods abandoned us! There was an error!'
        }
