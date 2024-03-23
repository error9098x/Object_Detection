import React, { useState, useEffect } from "react";
import axios from "axios";

const YouTubeVideoUpload = () => {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);
  const [frames, setFrames] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:5000/process_youtube_video");
    eventSource.onmessage = (event) => {
      if (event.data === "done") {
        eventSource.close();
      } else {
        setFrames((prevFrames) => [...prevFrames, event.data]);
      }
    };
    return () => {
      eventSource.close();
    };
  }, []);

  const handleYouTubeVideoUpload = async (e) => {
    e.preventDefault();

    if (!youtubeUrl) {
      console.error('Please provide a YouTube video URL.');
      return;
    }
    try {
      const response = await axios.post('http://localhost:5000/process_youtube_video', {
        youtube_url: youtubeUrl,
        confidence_threshold: confidenceThreshold,
      });
      // Assuming the server sends back an array of base64 strings
      setFrames(response.data.frames || []);
    } catch (error) {
      console.error('Error processing YouTube video:', error);
      setFrames([]); // Clear frames in case of error
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">YouTube Video Upload</h2>
      <form onSubmit={handleYouTubeVideoUpload}>
        <input
          type="text"
          value={youtubeUrl}
          onChange={(e) => setYoutubeUrl(e.target.value)}
          placeholder="Enter YouTube video URL"
          className="mb-4 border border-gray-300 rounded p-2"
        />
        <input
          type="number"
          step="0.1"
          value={confidenceThreshold}
          onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
          className="mb-4 border border-gray-300 rounded p-2"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Process YouTube Video
        </button>
      </form>
      <div className="mt-8 grid grid-cols-3 gap-4">
        {frames.map((frame, index) => (
          <img
            key={index}
            src={`data:image/jpeg;base64,${frame}`}
            alt={`Processed frame ${index}`}
            className="mb-4"
          />
        ))}
      </div>
    </div>
  );
};

export default YouTubeVideoUpload;