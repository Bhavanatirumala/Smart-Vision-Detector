def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '<html><head><title>Smart Vision Detector</title></head><body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;"><h1>Smart Vision Detector</h1><p>Advanced AI-powered vision detection</p><div style="background: white; color: #333; padding: 30px; border-radius: 15px; margin: 20px auto; max-width: 600px;"><h2 style="color: #28a745;">Deployment Successful!</h2><p>Your Smart Vision Detector is now live on Vercel!</p></div></body></html>'
    }