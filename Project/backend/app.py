from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import tempfile
import numpy as np
from pytube import YouTube
import os
import time
import base64
import json

app = Flask(__name__)
CORS(app)
model = YOLO('yolov8n.pt')

def frame_to_base64(frame):
    """Converts a single video frame to a base64 string."""
    retval, buffer = cv2.imencode('.jpg', frame)
    if retval:
        base64_str = base64.b64encode(buffer).decode('utf-8')
        return base64_str
    else:
        raise ValueError("Could not encode frame to base64.")

@app.route('/process_video', methods=['POST'])
def process_video():
    video_file = request.files['video']
    confidence_threshold = float(request.form.get('confidence_threshold', 0.5))

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(video_file.read())
        temp_file.file.close()  # Close the file to ensure it's written to disk

        cap = cv2.VideoCapture(temp_file.name)
        frame_skip = 5
        frame_count = 0

        def generate():
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_count % frame_skip == 0:
                    frame = cv2.resize(frame, (640, 480))  # You might need to adjust this
                    results = model.track(frame, persist=True, conf=confidence_threshold)
                    frame_ = results[0].plot()
                    frame_base64 = frame_to_base64(frame_)
                    yield f'data: {frame_base64}\n\n'
                    time.sleep(0.5)  # Delay between frames
                frame_count += 1
            cap.release()
            os.unlink(temp_file.name)
            yield 'data: done\n\n'  # Signal that the stream is done

        return Response(generate(), mimetype='text/event-stream')

@app.route('/process_youtube_video', methods=['POST'])
def process_youtube_video():
    youtube_url = request.json['youtube_url']
    confidence_threshold = request.json.get('confidence_threshold', 0.5)

    yt = YouTube(youtube_url)
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

    if video_stream:
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, f"{yt.video_id}.mp4")
        video_stream.download(output_path=temp_dir, filename=f"{yt.video_id}.mp4")

        cap = cv2.VideoCapture(temp_file_path)
        frame_skip = 5
        frame_count = 0

        def generate():
            nonlocal frame_count
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_count % frame_skip == 0:
                    frame = cv2.resize(frame, (640, 480))
                    results = model.track(frame, persist=True, conf=confidence_threshold)
                    frame_ = results[0].plot()
                    _, encoded_image = cv2.imencode('.jpg', frame_)
                    frame_base64 = base64.b64encode(encoded_image).decode('utf-8')
                    yield f'data: {json.dumps({"frame": frame_base64})}\n\n'
                    time.sleep(0.5)
                frame_count += 1
            cap.release()
            os.remove(temp_file_path)
            os.rmdir(temp_dir)
            yield 'data: done\n\n'

        return Response(generate(), mimetype='text/event-stream')

    else:
        return jsonify({"error": "Could not retrieve video stream."}), 400


@app.route('/process_image', methods=['POST'])
def process_image():
    image_file = request.files['image']
    confidence_threshold = float(request.form['confidence_threshold'])

    # Decode the image
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)  # Forcefully read as a 3-channel image
    img = cv2.resize(img, (640, 480))  # Reduce image resolution

    # Pass the image to the YOLO model
    results = model.track(img, conf=confidence_threshold)
    img_ = results[0].plot()

    # Convert the processed image to base64 string for JSON response
    _, encoded_image = cv2.imencode('.jpg', img_)
    base64_image = base64.b64encode(encoded_image.tostring()).decode('utf-8')

    return jsonify({'image': base64_image})

# @app.route('/process_youtube_video', methods=['POST'])
# def process_youtube_video():
#     youtube_url = request.json['youtube_url']
#     confidence_threshold = request.json['confidence_threshold']
#     frames_base64 = []

#     try:
#         yt = YouTube(youtube_url)
#         video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

#         if video_stream:
#             temp_dir = tempfile.mkdtemp()
#             temp_file_path = os.path.join(temp_dir, f"{yt.video_id}.mp4")
#             video_stream.download(output_path=temp_dir, filename=f"{yt.video_id}.mp4")

#             cap = cv2.VideoCapture(temp_file_path)
#             frame_skip = 5  # Same frame skipping logic as before
#             frame_count = 0

#             while True:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 if frame_count % frame_skip == 0:
#                     frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB) if frame.shape[2] == 4 else frame  # Convert to RGB if RGBA
#                     frame = cv2.resize(frame, (640, 480))
#                     results = model.track(frame, persist=True, conf=confidence_threshold)
#                     frame_ = results[0].plot()
#                     frame_base64 = frame_to_base64(frame_)
#                     frames_base64.append(frame_base64)
#                     time.sleep(0.4)
#                 frame_count += 1

#             cap.release()
#             os.remove(temp_file_path)
#             os.rmdir(temp_dir)
#         else:
#             return jsonify({"error": "Could not retrieve video stream."}), 400
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"error": "An error occurred"}), 500

#     return jsonify(frames_base64)

# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')