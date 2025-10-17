"""
Ultra-simple test function for Vercel
"""

def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Smart Vision Detector - Test</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
                .container { max-width: 600px; margin: 0 auto; }
                .success { background: #d4edda; padding: 20px; border-radius: 10px; color: #155724; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧠 Smart Vision Detector</h1>
                <div class="success">
                    <h2>✅ Deployment Successful!</h2>
                    <p>Your Smart Vision Detector is working on Vercel!</p>
                </div>
                <p>This is a simplified test version. The full app will be deployed once this works.</p>
            </div>
        </body>
        </html>
        '''
    }
