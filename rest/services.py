import hashlib
import logging
import traceback
from datetime import datetime as dtt
from django.core.mail import send_mail

from .enums import TokenType
from .models import Token
# from utils.constants import STATIC_VARS
from blog.utils.email_text import EmailTextEnum
# from utils.send_mail import send_action_required_mail
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)


def is_valid_time(create_date, deadline_time):
    """This function  validate the time of the hash code and otp for the user"""
    # try:
    dateFormat = '%Y-%m-%d %H:%M:%S'
    create_date = create_date.strftime(dateFormat)
    current_date = dtt.utcnow().strftime(dateFormat)
    current_date = dtt.strptime(current_date, dateFormat)
    create_date = dtt.strptime(create_date, dateFormat)
    timedelta = current_date - create_date
    time_difference = timedelta.days * 24 * 36000 + timedelta.seconds
    if time_difference <= (600 * deadline_time):
        return True
    else:
        return False

    # except Exception:
    #     logger.exception(traceback.format_exc())


def verifyOtpOrHash(user, comingToken, tokenType):
    """This function  verify the hash code and otp for the user"""
    # try:
    result = None
    try:
        tokenObj = Token.objects.get(user=user, token_type=tokenType)
    except:
        result = {"error": True, "message": "You never generate this request"}
        return result
    if not is_valid_time(tokenObj.created_at, tokenObj.expiry_minutes):
        result = {"error": True, "message": "This token is not expired."}
        return result
    if comingToken != tokenObj.token:
        result = {"error": True, "message": "This token is not a valid token."}
        return result
    result = {"error": False, "message": "This token is verify successfully."}
    return result
    # except Exception:
    #     logger.exception(traceback.format_exc())


def generate_hash(user):
    """This function generate a hash from the user data """
    # try:
    encoded_string = str(user.id) + user.email
    print(encoded_string,'ENCODED_STRING')
    encoded_string = encoded_string.encode('utf-8')
    print(encoded_string,'ENCODED_STRING')

    return str(hashlib.sha224(encoded_string).hexdigest())
    # except Exception:
    #     logger.exception(traceback.format_exc())


def save_token_data(tokeType, token, user, expiryMinutes):
    """This function used in the saving the token data in the token table."""
    # try:
    if not tokeType and not token and not user and not expiryMinutes:
        raise Exception("Invalid parameters")

    tokenData, created = Token.objects.get_or_create(
        token_type=tokeType.name,
        user=user,
    )
    tokenData.token = token
    tokenData.expiry_minutes = expiryMinutes
    tokenData.created_at = dtt.utcnow()
    print(tokenData,'Token_data')
    tokenData.save()
    return True
    # except Exception:
    #     logger.exception(traceback.format_exc())


def fill_dynamic_values_in_string(EmailType, user, data=None):
    """This function helps you in the make a dynamic string according to the email text and subject"""
    # try:
    if not EmailType and not user:
        raise Exception("Invalid parameters")

    emailTypeEnumValues = EmailType.value
    subject = emailTypeEnumValues.get("subject")
    emailText = str(emailTypeEnumValues.get("text"))

    if EmailType.name in EmailTextEnum.EMAIL_VERIFICATION_TEXT.name:
                          # EmailTextEnum.EMAIL_FORGET_PASSWORD_TEXT.name,
                          # EmailTextEnum.EMAIL_RESET_PASSWORD_TEXT.name]:
        print("ngchhhhhhhhhhh")
        emailText.format(URL=data)
        print(emailText)
        emailText.lstrip()
        return subject, emailText

    # except Exception:
    #     logger.exception(traceback.format_exc())


def prepare_activation_link(user, tokenType):
    """This function helps you to sending the dynamic link to the email verification"""
    # try:
    if not user:
        raise Exception("Invalid parameters")
    hashCode = generate_hash(user)
    save_token_data(tokenType, hashCode, user, 15)
    if tokenType == TokenType.EMAIL_VERIFICATION:
        link_suffix = "activate-email/{0}/{1}".format(user.id, hashCode)
        url = STATIC_VARS['frontend-url'] + link_suffix
        subject, email = fill_dynamic_values_in_string(EmailTextEnum.EMAIL_VERIFICATION_TEXT, user, data=url)
        print(subject,'SUBJECT')
        print(email,'EMAIL')
        print(user.email,'emailuser' )
        mial=user.email
        send_mail(
        'Email Verification',
        email,
        'arun.singh1@oodlestechnologies.com',
        [mial],


        fail_silently=False,
            )


LOCAL_STATIC_VARS = {

    'frontend-url': 'http://localhost:8000',

}
STATIC_VARS = LOCAL_STATIC_VARS


