from functools import wraps
from flask import session, request, redirect

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
