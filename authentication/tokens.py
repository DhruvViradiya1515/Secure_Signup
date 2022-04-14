from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# Token generation for creating unique link for email verification

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp))

generate_token  =TokenGenerator()
