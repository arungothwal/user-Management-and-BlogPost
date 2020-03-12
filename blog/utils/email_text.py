from enum import Enum


class EmailTextEnum(Enum):
    EMAIL_VERIFICATION_TEXT = {
        "subject": "Verify Your E-Mail.",
        "text": 'Hello User, <br/><br/>Please verify your email by clicking on below link. <br/><br/> <a href="{URL}">Click here for verification</a> <br/><br/> <b>Note: This link is expiries in 15 min.<b/>'
    }
