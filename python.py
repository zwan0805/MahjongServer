import os
from flask import Flask, request, jsonify
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('best_154.pt')


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    img = Image.open(file.stream)
    results = model.predict(source=img)
    ret = []
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for i, box in enumerate(boxes):
            ret.append(result.names[int(box.cls)])
            
    return jsonify({"msg": "success", "result": ",".join(ret)})


if __name__ == '__main__':
    ssl_cert = 'C:\Openssl\certificate.crt' 
    ssl_key = 'C:\Openssl\private_key.key'   
    context = (ssl_cert, ssl_key) 
    app.run(host='192.168.53.207', port=6666, ssl_context=context, debug=True)
