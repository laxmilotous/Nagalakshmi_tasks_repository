from config import app
@app.route('/',methods=['GET'])
def greet():
    return "<b> My application is Running..<b>"