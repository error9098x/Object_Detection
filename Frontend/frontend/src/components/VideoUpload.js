import React, { useState } from 'react';
import axios from 'axios';

const VideoUpload = () => {
  const [video, setVideo] = useState(null);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);
  const [frames, setFrames] = useState([]);

  const handleVideoUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('video', video);
    formData.append('confidence_threshold', confidenceThreshold);

    try {
      const response = await axios.post('http://localhost:5000/process_video', formData);
      setFrames(response.data);
    } catch (error) {
      console.error('Error processing video:', error);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Video Upload</h2>
      <form onSubmit={handleVideoUpload}>
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setVideo(e.target.files[0])}
          className="mb-4"
        />
        <input
          type="number"
          step="0.1"
          value={confidenceThreshold}
          onChange={(e) => setConfidenceThreshold(e.target.value)}
          className="mb-4 border border-gray-300 rounded p-2"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Process Video
        </button>
      </form>
      <div className="mt-8">
        {frames.map((frame, index) => (
          <img
            key={index}
            src={`data:image/jpeg;base64,${frame}`}
            alt={`Frame ${index}`}
            className="mb-4"
          />
        ))}
      </div>
    </div>
  );
};

export default VideoUpload;