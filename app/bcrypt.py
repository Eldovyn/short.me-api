from flask_bcrypt import Bcrypt
from . import create_app

app = create_app()
bcrypt = Bcrypt(app)
