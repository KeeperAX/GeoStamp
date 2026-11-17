from django.core import signing

SALT = 'geostamp-email-verification'
TOKEN_MAX_AGE = 86400


def create_verification_token(user):
    return signing.dumps(
        {
            'user_id': user.id,
            'email': user.email,
            'password': user.password
        },
        salt=SALT,
    )


def read_verification_token(token):
    return signing.loads(
        token,
        salt=SALT,
        max_age=TOKEN_MAX_AGE,
    )