from config import app, client
from flask import request


@app.route('/upload-image', methods=['POST'])
def upload_image():
    bucket = 'eleventaskbucket'
    content_type = request.mimetype
    obj = request.files['file']
    filename = obj.filename
    client.put_object(Body=obj,
                      Bucket=bucket,
                      Key=filename,
                      ContentType=content_type
                      )

    return {'Image/File Uploaded Successfully': 'file uploaded'}, 200
