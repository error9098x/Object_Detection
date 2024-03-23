import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);
  const [processedImage, setProcessedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleImageUpload = async (e) => {
    e.preventDefault();

    if (!image) {
      alert('Please select an image to upload.');
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append('image', image);
    formData.append('confidence_threshold', confidenceThreshold);

    try {
      const response = await axios.post(
        'http://localhost:5000/process_image',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setProcessedImage(`data:image/jpeg;base64,${response.data.image}`);
    } catch (error) {
      console.error('Error processing image:', error);
      alert('An error occurred while processing the image.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Image Upload</h2>
      <form onSubmit={handleImageUpload}>
        <div className="mb-4">
          <label htmlFor="image" className="block mb-2 font-medium">
            Select an image:
          </label>
          <input
            type="file"
            id="image"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
            className="border border-gray-300 rounded p-2 w-full"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="threshold" className="block mb-2 font-medium">
            Confidence Threshold:
          </label>
          <input
            type="number"
            id="threshold"
            step="0.1"
            min="0"
            max="1"
            value={confidenceThreshold}
            onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
            className="border border-gray-300 rounded p-2 w-full"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-300"
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Process Image'}
        </button>
      </form>
      {processedImage && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-4">Processed Image:</h3>
          <img src={processedImage} alt="Processed" className="max-w-full h-auto rounded" />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;