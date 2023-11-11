def lambda_handler(event, context):
    print('Hello world, doing ci/cd testing.')
    return {
        'event': event,
        'context': context,
        'status': 200
    }