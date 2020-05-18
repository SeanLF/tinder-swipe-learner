import functools
import fileinput, re

from flask import Blueprint, g, render_template, request, session, url_for, redirect

from tinder_token.phone import TinderTokenPhoneV2
import tinder_api_sms

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    tinder_token = session.get('tinder_token')

    if tinder_token is None:
        g.user = None
    else:
        g.user = tinder_token
        g.phone_number = session.get('phone_number')

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
      return render_template('auth/sms.html')
  else:
      phone = TinderTokenPhoneV2()
      session['phone_number'] = request.form['phone_number']
      phone.send_otp_code(session.get('phone_number'))
      return redirect(url_for('auth.sms_otp_code'))

@bp.route('/login/sms_otp_code', methods=['GET', 'POST'])
def sms_otp_code():
  if request.method == 'GET':
      return render_template('auth/sms_otp_code.html')
  else:
      phone = TinderTokenPhoneV2()
      # if code present, then user logging in, else only get new tinder token
      if 'otp_code' in request.form:
          otp_code = request.form['otp_code']
          session['refresh_token'] = phone.get_refresh_token(otp_code, session.get('phone_number'))
      session['tinder_token'] = phone.get_tinder_token(session.get('refresh_token'))
      persist_tinder_token(session.get('tinder_token'))
      return redirect(url_for('index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def persist_tinder_token(tinder_token):
  
  pattern = r'^tinder_token.*'
  new_value = f"tinder_token = '{tinder_token}'"
  with fileinput.FileInput('config.py', inplace=True) as file:
      for line in file:
          print(re.sub(pattern, new_value, line))
