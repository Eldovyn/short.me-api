from ..task import send_email_task
from ..config import web_short_me


class SendEmail:
    @staticmethod
    def send_email_verification(user_data, token_email):
        send_email_task.apply_async(
            args=[
                "Account Active",
                [user_data.email],
                f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user_data.username},</p>
    <p>Someone has requested a link to verify your account, and you can do this through the link below.</p>
    <p>
        <a href="{web_short_me}/account-active?token={token_email}">
            Click here to activate your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                """,
            ],
        )

    @staticmethod
    def send_email_reset_password(user_data, token_email):
        send_email_task.apply_async(
            args=[
                "Reset Password",
                [user_data.email],
                f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user_data.username},</p>
    <p>Someone has requested a link to reset password your account, and you can do this through the link below.</p>
    <p>
        <a href="{web_short_me}/reset-password?token={token_email}">
            Click here to reset password your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                """,
            ],
        )
