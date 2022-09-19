"""
Defines the blueprint for the auth for admin and user
"""
from flask import Blueprint

from ..resources import AuthResource

AUTH_BLUEPRINT = Blueprint("auth", __name__)

AUTH_BLUEPRINT.route("/login-user", methods=['POST'])(AuthResource.login_user)
