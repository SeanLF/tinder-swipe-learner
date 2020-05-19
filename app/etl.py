from flask import Blueprint

bp = Blueprint('etl', __name__, url_prefix='/etl')

@bp.route('/')
def index():
  from multiprocessing import Process
  from .tinder import get_tinder_recommendations
  profiles = get_tinder_recommendations()
  p = Process(target=etl, args=(profiles,))
  p.start()
  return 200

def etl(profiles):
  from threading import Thread
  for profile in profiles:
    t = Thread(target=extract_images, args=(profile))
    t.start()
    
def extract_images(profile):
  from .tinder import parse_images
  for image in parse_images(profile['images']):
    if image_accessible(image):
      downloaded_image = download_image(image, profile['class'])
      if image_contains_face(downloaded_image) == False:
        discard_image(downloaded_image)
        
def image_accessible(image):
  import requests
  try:
    r = requests.head(image)
    return r.status_code == 200
    # prints the int of the status code. Find more at httpstatusrappers.com :)
  except requests.ConnectionError:
    print("failed to connect")
    return False

def download_image(image, klass):
  import urllib.request
  urllib.request.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")

def image_contains_face(image):
  import face_recognition
  image = face_recognition.load_image_file(image)
  return len(face_recognition.face_locations(image)) > 0

def discard_image(image_path):
  import os
  os.remove(image_path)
