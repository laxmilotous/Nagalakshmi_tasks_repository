from orm.models import User
from config import db, app, client
from flask import jsonify, request


@app.route("/register", methods=['POST'])
def register():
    bucket = 'python-bucket77'
    content_type = request.mimetype
    userid = request.form['userid']
    name = request.form['name']
    city = request.form['city']
    age = request.form['age']
    obj = request.files['pic']
    profilepic = obj.filename
    print(age)
    # data=request.get_json()
    # print(data)
    user = User(userid, name, city, age, profilepic)
    db.session.add(user)
    db.session.commit()
    client.put_object(Body=obj,
                      Bucket=bucket,
                      Key=userid,
                      ContentType=content_type
                      )
    return {"status": "insertion success"}, 201


@app.route("/user/<string:userid>", methods=['GET'])
def download_pp(userid):
    user = User.query.filter(User.userid == userid).first()
    print(user)
    client.download_file('python-bucket77', userid, "e:\\downloads\\"+userid)
    return jsonify(user.serialize())
