from django.contrib.auth.base_user import AbstractBaseUser
from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class generatetoken(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)
    
token_generator = generatetoken()