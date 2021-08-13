from lps import app
from lps.config import Config


app.config.from_object(Config)

if __name__ == '__main__':
    app.run(host="localhost", port=5000)