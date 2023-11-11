def lambda_handler(event, context):
    print('Hello world')
    return {
        'event': event,
        'context': context,
        'status': 200
    }