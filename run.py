from portal import app
import os

app.secret_key = os.urandom(24)

