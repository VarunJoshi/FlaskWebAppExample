import logging
import os
import subprocess
import time
from flask import Flask, request, render_template, jsonify
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.error('No file part in the form')
            return 'No file part in the form', 400
        file = request.files['file']
        if file.filename == '':
            logging.error('No file selected')
            return 'No file selected', 400
        if file and 'times' in request.form:
            save_path = 'uploads'  # specify the path to save the file
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            filename = file.filename
            filepath = os.path.join(save_path, filename)
            # save the file in chunks
            chunk_size = 1024  # you can adjust this value depending on your needs
            with open(filepath, 'wb') as f:
                chunk = file.read(chunk_size)
                while len(chunk) > 0:
                    f.write(chunk)
                    chunk = file.read(chunk_size)
            numOfTimes = int(request.form['times'])
            thread = Thread(target=run_script, args=(filepath, numOfTimes))
            thread.start()
            logging.info(f"File uploaded and saved to {filepath}. Starting script with {numOfTimes} times.")
            return jsonify({}), 202
    return render_template('upload.html')

def run_script(filepath, numOfTimes):
    try:
        logging.info(f"Running script with filepath: {filepath} and numOfTimes: {numOfTimes}")
        subprocess.run(["python", "C:/ACStressTest/DropCommandsUsingCLITool.py", filepath, str(numOfTimes)], check=True, shell=True)
        logging.info("Script completed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running the script: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# The app.run line is removed or commented out for production deployment
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5050, debug=True)