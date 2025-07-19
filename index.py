from flask_app import app

# For Vercel deployment
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == "__main__":
    app.run()
