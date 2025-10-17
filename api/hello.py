def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '<html><body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0;"><h1>Hello from Vercel!</h1><p>Smart Vision Detector is working!</p></body></html>'
    }