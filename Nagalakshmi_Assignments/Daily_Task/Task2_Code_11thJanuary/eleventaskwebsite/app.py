from config import app
from flask import Flask


import bucketinfo


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
