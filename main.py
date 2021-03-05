#!/usr/local/bin/python3
import settings
import headlines
if __name__ == '__main__':
    headlines.app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG)
