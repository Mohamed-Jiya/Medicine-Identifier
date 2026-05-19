# from flask import Flask, render_template, request, jsonify
# from main import identify_medicine
# import os

# app = Flask(__name__)

# # open the main page
# @app.route('/')
# def home():
#     return render_template('index.html')

# # receive image and return medicine info
# @app.route('/identify', methods=['POST'])
# def identify():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image uploaded!"})

#     image = request.files['image']

#     # save image temporarily
#     image_path = "temp_upload.jpg"
#     image.save(image_path)

#     # run your OCR pipeline
#     result = identify_medicine(image_path)

#     # delete temp image after reading
#     os.remove(image_path)

#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from main import identify_medicine
from database import search_medicine
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# image upload route
@app.route('/identify', methods=['POST'])
def identify():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded!"})
    image = request.files['image']
    image_path = "temp_upload.jpg"
    image.save(image_path)
    result = identify_medicine(image_path)
    os.remove(image_path)
    return jsonify(result)

# search by name route
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    name = data.get('name', '')
    result = search_medicine(name)
    if result:
        return jsonify({
            "name":        result[1],
            "use":         result[2],
            "side_effect": result[3],
            "dosage":      result[4]
        })
    else:
        return jsonify({"error": f"'{name}' not found in database!"})

if __name__ == '__main__':
    app.run(debug=True)