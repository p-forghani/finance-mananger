from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def get_serializer():
    # You can reuse the app's secret key directly here
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
