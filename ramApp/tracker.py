import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from ramApp.db import get_db
from ramApp.auth import login_required

bp = Blueprint('tracker', __name__)

@bp.route('/')
@login_required
def home():
    #db = get_db()
    
    return render_template('tracker/home.html')