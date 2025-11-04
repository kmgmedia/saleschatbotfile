import json

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'status': 'ok',
            'message': 'ShopBot Webhook Server is running!',
            'endpoints': {
                'webhook': '/api/webhook',
                'health': '/api/index'
            }
        }, indent=2)
    }
