from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from utils import allowed_file, check_resolution
from model_predict import analyze_image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '../data/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Нет файла с именем file'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Недопустимый формат файла'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    if not check_resolution(filepath):
        os.remove(filepath)
        return jsonify({'error': 'Низкое разрешение изображения'}), 400

    return jsonify({'message': 'Файл успешно загружен', 'filename': filename}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Не указано имя файла'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Файл не найден'}), 404

    result = analyze_image(filepath)
    return jsonify(result), 200

@app.route('/export', methods=['GET'])
def export_csv():
    import pandas as pd
    data = [
        {"patient_id": 1, "age": 45, "gender": "M", "risk_level": "high"},
        {"patient_id": 2, "age": 60, "gender": "F", "risk_level": "low"},
    ]
    df = pd.DataFrame(data)
    csv_path = "../data/csv/patient_export.csv"
    df.to_csv(csv_path, index=False)
    return jsonify({"message": "Экспорт завершён", "file": csv_path})

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
