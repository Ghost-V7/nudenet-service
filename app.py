# nudenet-service/app.py

import os
from flask import Flask, request, jsonify
from nudenet import NudeDetector

# Initialize our Flask web application
app = Flask(__name__)

# Initialize the NudeDetector.
# This will download the model the first time it's run, which can take a moment.
print("Initializing NudeDetector...")
nude_detector = NudeDetector()
print("NudeDetector initialized.")

# Define our API endpoint. It will only accept POST requests.
@app.route('/detect', methods=['POST'])
def detect():
    # Check if an 'image' file was sent in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    # Make sure the file has a name
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to a temporary location so NudeNet can process it
    temp_path = os.path.join("/tmp", file.filename)
    file.save(temp_path)

    try:
        # Run the detection!
        print(f"Detecting nudity in {temp_path}...")
        results = nude_detector.detect(temp_path)
        print(f"Detection complete. Results: {results}")
        
        # Clean up the temporary file
        os.remove(temp_path)

        # Send the results back as JSON
        return jsonify(results)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Clean up even if there's an error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500

# A simple "health check" route to make sure the server is running
@app.route('/')
def health_check():
    return "NudeNet service is alive!"

# This makes the app runnable
if __name__ == '__main__':
    # We use Gunicorn in production, so this is mainly for local testing
    app.run(host='0.0.0.0', port=10000)