import random
import string

class PasswordGenerator:
    @staticmethod
    def generate_password(length=12) -> str:
        """Generate strong password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        while True:
            password = ''.join(random.choice(chars) for _ in range(length))
            if (
                len(password) >= 8 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*" for c in password)
            ):
                return password