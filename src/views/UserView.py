#/src/views/UserView

from distutils.log import error
from random import randrange
from flask import request, json, Response, Blueprint, g, session
from marshmallow import ValidationError
from ..models.UserModel import UserModel, UserSchema
from ..models.TalentModel import *
from ..models.ProfileModel import *
from ..models.CompanyModel import *
from ..models.VideoModel import *
from ..shared.Authentication import Auth
from ..shared.CustomService import custom_response
import smtplib

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

gmail_user = 'appc31058@gmail.com'
gmail_password = ''

@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  print(req_data)
  try:
    data = user_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  print(user_schema.dump(user_in_db).get('verify_code'))
  if user_in_db :
    if user_schema.dump(user_in_db).get('register_status'):
      message = {'error': 'User already exist, please supply another email address'}
      return custom_response(message, 400)
    else :
      user = UserModel(data)
      user.update(data)
      sms_code_send(user_schema.dump(user_in_db).get('verify_code'),user_schema.dump(user_in_db).get('email') )
      return custom_response({'status': 'success'}, 200)    
    
  user = UserModel(data)
  user.save()
  ser_data = user_schema.dump(user)
  print("=======================")
  print(ser_data.get('id'))
  # token = Auth.generate_token(ser_data.get('id'))
  # print(token)
  sms_code_send(ser_data.get('verify_code'),ser_data.get('email') )
  return custom_response({'status': 'success'}, 200)

@user_api.route('/verify', methods=['POST'])
def verify():
  """
  Create User Function
  """
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db

  user_in_db = UserModel.get_user_by_email(data.get('email'))
  update_user = user_schema.dump(user_in_db)
  print(update_user)
  # for key, item in update_user.items():
  if user_schema.dump(user_in_db).get('verify_code') != data.get('verify_code'):
    message = {'error': 'Failed Verify code, Please check code in your email'}
    return custom_response(message, 400)
  data['register_status'] = True
  print(update_user)

  # setattr(data, key, item)
  # user = UserModel(user_in_db)
  user_in_db.update(data)
  print("=======================")
  print(update_user.get('id'))
  token = Auth.generate_token(update_user.get('id'))
  # session['username'] = update_user.get('id')
  print(token)
  return custom_response({'jwt_token': token,'id':update_user.get('id'),'email':update_user.get('email'),'type':update_user.get('type'), 'status':'success'}, 200)

@user_api.route('/resend', methods=['POST'])
def resend():
  """
  Create User Function
  """
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  update_user = user_schema.dump(user_in_db)
  print(update_user)
  # for key, item in update_user.items():
  # if user_schema.dump(user_in_db).get('verify_code') != data.get('verify_code'):
  #   message = {'error': 'Failed Verify code, Please check code in your email'}
  #   return custom_response(message, 400)
  update_user['verify_code'] = randrange(1000,9999,4)
  user_in_db.update(update_user)
  sms_code_send(update_user['verify_code'],update_user['email'] )
  print(update_user)

  # setattr(data, key, item)
  # user = UserModel(user_in_db)

  return custom_response({'status': 'success'}, 200)

@user_api.route('/talents_all/<int:page_num>/<int:page_length>', methods=['GET'])
def get_talent_all(page_num, page_length):
  """
  Get all users
  """
  users = UserModel.get_talents_by_page_num(page_num,page_length)
  ser_users = user_schema.dump(users.items, many=True)
  res_talent_data = []
  for ser_user in ser_users:
    if (ser_user.get('type') == 'talent'):
      talent = TalentModel.get_talent_by_userid(ser_user.get('id'))
      profile = ProfileModel.get_profile_by_userid(ser_user.get('id'))
      video = VideoModel.get_video(ProfileSchema().dump(profile).get('video_id'))
      
      if talent:
        talent_data = TalentSchema().dump(talent)
        talent_data.pop('id')
        talent_data.pop('user_id')
        ser_user.update(talent_data)

      if profile:
        profile_data = ProfileSchema().dump(profile)
        profile_data.pop('id')
        profile_data.pop('user_id')
        ser_user.update(profile_data)

      if video:
        video_data = VideoSchema().dump(video)
        video_data.pop('id')
        video_data.pop('type')
        ser_user.update(video_data)

      ser_user['status'] = 'success'
      ser_user.pop('verify_code')
      res_talent_data.append(ser_user)      
  return custom_response(res_talent_data, 200)

@user_api.route('/company_all/<int:page_num>/<int:page_length>', methods=['GET'])
def get_company_all(page_num, page_length):
  """
  Get all users
  """
  users = UserModel.get_companies_by_page_num(page_num, page_length)
  ser_users = user_schema.dump(users.items, many=True)
  res_company_data = []
  for ser_user in ser_users:
    if (ser_user.get('type') == 'company'):
      company = CompanyModel.get_company_by_userid(ser_user.get('id'))
      profile = ProfileModel.get_profile_by_userid(ser_user.get('id'))
      video = VideoModel.get_video(ProfileSchema().dump(profile).get('video_id'))

      if company:
        company_data = CompanySchema().dump(company)
        company_data.pop('id')
        company_data.pop('user_id')
        ser_user.update(company_data)

      if profile:
        profile_data = ProfileSchema().dump(profile)
        profile_data.pop('id')
        profile_data.pop('user_id')
        ser_user.update(profile_data)

      if video:
        video_data = VideoSchema().dump(video)
        video_data.pop('id')
        video_data.pop('type')
        ser_user.update(video_data)

      ser_user['status'] = 'success'
      ser_user.pop('verify_code')
      res_company_data.append(ser_user)
  return custom_response(res_company_data, 200)

@user_api.route('/companies_count', methods=['GET'])
def get_companies_count():
  companies_count = UserModel.get_companies_count()
  print(companies_count)
  res_data = {}
  res_data['count'] = companies_count
  res_data['status'] = 'success'
  return custom_response(res_data, 200)


@user_api.route('/talents_count', methods=['GET'])
def get_talents_count():
  companies_count = TalentModel.get_talents_count()
  res_data = {}
  res_data['count'] = companies_count
  res_data['status'] = 'success'
  return custom_response(res_data, 200)
 
@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
  """
  Get a single user
  """
  user = UserModel.get_one_user(user_id)
  
  if not user:
    return custom_response({'error': 'user not found'}, 400)
  
  ser_user = user_schema.dump(user)
  print(ser_user)
  if (ser_user.get('type') == 'company'):
    company = CompanyModel.get_company_by_userid(user_id)
    profile = ProfileModel.get_profile_by_userid(user_id)
    video = VideoModel.get_video(ProfileSchema().dump(profile).get('video_id'))

    company_data = CompanySchema().dump(company)
    company_data.pop('id')
    company_data.pop('user_id')

    profile_data = ProfileSchema().dump(profile)
    profile_data.pop('id')
    profile_data.pop('user_id')

    video_data = VideoSchema().dump(video)
    video_data.pop('id')
    video_data.pop('type')

    ser_user.update(company_data)
    ser_user.update(profile_data)
    ser_user.update(video_data)
    ser_user['status'] = 'success'
    ser_user.pop('verify_code')
  if (ser_user.get('type') == 'talent'):
    talent = TalentModel.get_talent_by_userid(user_id)
    profile = ProfileModel.get_profile_by_userid(user_id)
    video = VideoModel.get_video(ProfileSchema().dump(profile).get('video_id'))

    talent_data = TalentSchema().dump(talent)
    talent_data.pop('id')
    talent_data.pop('user_id')

    profile_data = ProfileSchema().dump(profile)
    profile_data.pop('id')
    profile_data.pop('user_id')

    video_data = VideoSchema().dump(video)
    video_data.pop('id')
    video_data.pop('type')

    ser_user.update(company_data)
    ser_user.update(profile_data)
    ser_user.update(video_data)
    ser_user['status'] = 'success'
    ser_user.pop('verify_code')
  return custom_response(ser_user, 200)


@user_api.route('/update/<int:id>', methods=['PUT'])
@Auth.auth_required
def update(id):
  """
  Update me
  """
  req_data = request.get_json()
  data = user_schema.load(req_data, partial=True)

  user = UserModel.get_one_user(id)
  user.update(data)
  ser_user = user_schema.dump(user)
  ser_user['status'] = 'success'
  return custom_response(ser_user, 200)

@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a user
  """
  user = UserModel.get_one_user(g.user.get('id'))
  user.delete()
  return custom_response({'message': 'deleted'}, 204)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  """
  Get me
  """
  user = UserModel.get_one_user(g.user.get('id'))
  ser_user = user_schema.dump(user)
  ser_user['status'] = 'success'
  return custom_response(ser_user, 200)

@user_api.route('/talents/<int:page_num>/<int:page_length>', methods=['GET'])
def get_talents_by_page_num(page_num,page_length):
  try:
    talents = UserModel.get_talents_by_page_num(page_num,page_length)
  except ValidationError as error:
    print('failed')
    print(error.messages)
    return custom_response(error,400)
  if not talents:
    return custom_response({'error':'There is not any talents'},400 )
  res_data = user_schema.dump(talents.items, many=True)
  return custom_response(res_data, 200)
  


@user_api.route('/login', methods=['POST'])
def login():
  """
  User Login Function
  """
  req_data = request.get_json()
  print(req_data)
  
  try:
    data = user_schema.load(req_data, partial=True)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  print(data)
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  user = UserModel.get_user_by_email(data.get('email'))
  ser_data = user_schema.dump(user)
  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  if ser_data.get('register_status') != True:
    print("failed")
    return custom_response({'error':'you did not verify with sms_code, Please sign up with this eamil'},400)
  token = Auth.generate_token(ser_data.get('id'))
  # session['username'] = ser_data.get('id')
  return custom_response({'jwt_token': token, "id":ser_data.get('id'), "email":ser_data.get('email'), "type":ser_data.get('type'), 'status':'success'}, 200)

@user_api.route('/admin/login', methods=['POST'])
def admin_login():
  """
  User Login Function
  """
  req_data = request.get_json()
  print(req_data)
  
  try:
    data = user_schema.load(req_data, partial=True)
  except ValidationError as error:
    print("ERROR: package.json is invalid")
    print(error.messages)
    return custom_response(error, 400)
  # if error:
  #   return custom_response(error, 400)
  print(data)
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  user = UserModel.get_user_by_email(data.get('email'))
  ser_data = user_schema.dump(user)
  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  if ser_data.get('type') !='admin':
    print("failed")
    return custom_response({'error':'you are not admin'},400)
  token = Auth.generate_token(ser_data.get('id'))
  # session['username'] = ser_data.get('id')
  return custom_response({'jwt_token': token, "id":ser_data.get('id'), "email":ser_data.get('email'), "type":ser_data.get('type'), 'status':'success'}, 200)

def sms_code_send(sms_code, to_address):
  print(sms_code, to_address)
  subject = "SMS Verify"
  body = "Please check sms code to login, SMS_CODE: %s" % sms_code
  email_text = """\
  From: %s
  To: %s
  Subject: %s

  %s
  """ % (gmail_user, to_address, subject, body)
  try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(gmail_user, to_address, email_text)
    smtp_server.close()
    print("Email sent successfully!")
    return custom_response({'status':'success'},200)
  except Exception as ex:
    print("Something went wrong….",ex)  
    return custom_response({'error':ex},400)

# @user_api.route('/logout', method=['POST'])
# @Auth.auth_required

# def logout():
#   if 'username' in session:
#     session.pop('username', None)
#   return custom_response({'status':'success'}, 200)

