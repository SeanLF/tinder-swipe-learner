import functools
import fileinput, re

from flask import Blueprint, g, render_template, request, session, url_for, redirect

from tinder_api import Tinder_API

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    if request.endpoint != 'static':
        g.tinder_token = session.get('tinder_token', None)
        if g.tinder_token is not None:
            g.phone_number = session.get('phone_number')


@bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
      return render_template('auth/sms.html')
  else:
      tinder_api = Tinder_API()
      session['phone_number'] = request.form['phone_number']
      tinder_api.send_otp_code(session.get('phone_number'))
      return redirect(url_for('auth.sms_otp_code'))


@bp.route('/login/sms_otp_code', methods=['GET', 'POST'])
def sms_otp_code():
  if request.method == 'GET':
      return render_template('auth/sms_otp_code.html')
  else:
      # if code present, then user logging in, else only get new tinder token
      if 'otp_code' in request.form:
          otp_code = str(request.form['otp_code'])
          session['refresh_token'] = Tinder_API().get_refresh_token(session.get('phone_number'), otp_code)
      refresh_api_token()
      return redirect(url_for('tinder.index'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.tinder_token is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def refresh_api_token():
    if 'refresh_token' in session and session['refresh_token'] is not None:
        from datetime import datetime, timedelta

        now = datetime.utcnow()
        one_day = timedelta(days=1)
        token_expiry_date = datetime.fromisoformat(session.get('tinder_token_exp_time', (now-one_day).isoformat()))

        # If we are past the expiration date of the token, renew it.
        if token_expiry_date <= now or session['tinder_token'] is None:
            print('condition entered')
            session['tinder_token'] = Tinder_API().get_api_token(session.get('refresh_token'))
            session['tinder_token_exp_time'] = (now + one_day).isoformat()