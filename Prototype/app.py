import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import numpy as np
from pytube import YouTube
import os
import time
st.title("Object Tracking App")
st.write("Upload a video or image file, or provide a YouTube video URL to track objects using YOLOv8.")
st.session_state['youtube_url'] = ''
sample_video_yt = "https://www.youtube.com/watch?v=TzPwQbH9zvE"
if st.button('Use Sample YouTube Video'):
    youtube_url = sample_video_yt
    st.session_state['youtube_url'] = youtube_url

uploaded_file = st.file_uploader("Choose a file", type=["mp4", "jpg", "jpeg", "png"])
youtube_url = st.text_input("Or enter a YouTube video URL",st.session_state['youtube_url'])

confidence_threshold = st.slider("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

model = YOLO('yolov8n.pt')

def process_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(video_file.read())
        cap = cv2.VideoCapture(temp_file.name)
        
        stframe = st.empty()
        frame_skip = 5  # Display only every 5th frame
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_skip == 0:
                frame = cv2.resize(frame, (640, 480))  # Reduce image resolution
                results = model.track(frame, persist=True, conf=confidence_threshold)
                frame_ = results[0].plot()
                time.sleep(0.4)  # Add a small delay to allow image display
                stframe.image(frame_, channels="BGR", use_column_width=True)
            frame_count += 1
        cap.release()
        os.unlink(temp_file.name)

def process_image(image_file):
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), 1)
    img = cv2.resize(img, (640, 480))  # Reduce image resolution
    results = model.track(img, conf=confidence_threshold)
    img_ = results[0].plot()
    st.image(img_, channels="BGR", use_column_width=True)



def process_youtube_video(url):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        
        if video_stream:
            temp_dir = "temp_yt_videos"
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.join(temp_dir, f"{yt.video_id}.mp4")
            video_stream.download(output_path=temp_dir, filename=f"{yt.video_id}.mp4")
            
            cap = cv2.VideoCapture(temp_file_path)
            stframe = st.empty()
            frame_skip = 5  # Display only every 5th frame
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_count % frame_skip == 0:
                    frame = cv2.resize(frame, (640, 480))  # Reduce image resolution
                    results = model.track(frame, persist=True, conf=confidence_threshold)
                    frame_ = results[0].plot()
                    stframe.image(frame_, channels="BGR", use_column_width=True)
                    time.sleep(0.4)  # Add a small delay to allow image display
                frame_count += 1
            cap.release()
            os.remove(temp_file_path)
        else:
            st.error("Could not retrieve video stream.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if uploaded_file is not None:
    if uploaded_file.type.startswith('video'):
        process_video(uploaded_file)
    elif uploaded_file.type.startswith('image'):
        process_image(uploaded_file)
    else:
        st.write("Unsupported file type. Please upload a video or image file.")
elif youtube_url:
    process_youtube_video(youtube_url)