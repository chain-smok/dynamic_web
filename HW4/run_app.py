import os
from hw4_app import app
if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(ssl_context=('server.crt','server.key'), port=port)