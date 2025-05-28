from flask_dance.contrib.google import make_google_blueprint, google
from flask import redirect, url_for, session, flash, current_app as app
from flask_dance.consumer import oauth_authorized
from db.models.models import db, User

import os

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/calendar.events"
    ],
    redirect_url="/google_oauth_callback"
)

# @oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Nie udało się zalogować przez Google (brak tokenu).", "danger")
        return False
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Nie udało się pobrać informacji o użytkowniku z Google.", "danger")
        return False

    user_info = resp.json()
    email = user_info["email"]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            email=email,
            password_hash="",
            first_name=user_info.get("given_name", ""),
            last_name=user_info.get("family_name", ""),
            is_email_confirmed=True
        )
        db.session.add(user)
        db.session.commit()
    session["user_id"] = user.id
    flash("Zalogowano przez Google!", "success")
    return False