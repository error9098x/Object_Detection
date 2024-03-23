import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import ImageUpload from './components/ImageUpload';
import YouTubeVideoUpload from './components/YouTubeVideoUpload';

const App = () => {
  const [selectedOption, setSelectedOption] = useState(null);

  const renderUploadComponent = () => {
    switch (selectedOption) {
      case 'video':
        return <VideoUpload />;
      case 'image':
        return <ImageUpload />;
      case 'youtube':
        return <YouTubeVideoUpload />;
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-indigo-600">Object Detection App</h1>
        <p className="text-gray-600">Powered by React JS + Flask</p>
      </header>

      <main className="flex flex-col items-center justify-center w-full max-w-4xl p-8 bg-white rounded-lg shadow-lg">
        {!selectedOption && (
          <>
            <div className="mb-8 text-center">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Upload Options</h2>
              <p className="text-gray-600">Choose one of the following options to upload your media:</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
              <button className="bg-indigo-100 rounded-lg p-6 flex flex-col items-center justify-center" onClick={() => setSelectedOption('video')}>
                <p className="text-gray-600 mt-4">Upload video from your device</p>
              </button>

              <button className="bg-green-100 rounded-lg p-6 flex flex-col items-center justify-center" onClick={() => setSelectedOption('image')}>
                <p className="text-gray-600 mt-4">Upload image from your device</p>
              </button>

              <button className="bg-red-100 rounded-lg p-6 flex flex-col items-center justify-center" onClick={() => setSelectedOption('youtube')}>
                <p className="text-gray-600 mt-4">Upload video from YouTube</p>
              </button>
            </div>
          </>
        )}

        {selectedOption && (
          <div className="w-full">
            <button className="mb-4 text-sm text-indigo-600" onClick={() => setSelectedOption(null)}>Back to options</button>
            {renderUploadComponent()}
          </div>
        )}
      </main>

      <footer className="mt-8 text-gray-600 text-center">
        <p>&copy; 2024 Object Detection App For IISC Internship</p>
      </footer>
    </div>
  );
};

export default App;