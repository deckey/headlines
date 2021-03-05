#!/usr/local/bin/python3
import settings
from headlines import app

def headlines(request):
    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG)
