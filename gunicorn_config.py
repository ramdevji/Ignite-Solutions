workers = 3

bind = "0.0.0.0:5000"

timeout = 30

loglevel = "info"

accesslog = "-"

errorlog = "-"

wsgi_app = "app:create_app()"  # Assuming your main file is app.py
