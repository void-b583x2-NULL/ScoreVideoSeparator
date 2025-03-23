import React, { useState } from 'react';
import './App.css'; // Assuming this is where the scrollable gallery styles are defined
import ImageUploader from './ImageUploader';
import ImageGallery from './ImageGallery';

const Annotator: React.FC = () => {
  const [images, setImages] = useState<string[]>([]);

  const handleImageUpload = (newImages: string[]) => {
    setImages(prevImages => [...prevImages, ...newImages]);
  };

  const handleRemoveImage = (imageToRemove: string) => {
    setImages(prevImages => prevImages.filter(image => image !== imageToRemove));
  };

  return (
    <div className="App">
      <h1>Image Gallery</h1>
      <ImageUploader onUpload={handleImageUpload} />
      {/* Scrollable gallery container */}
      <div className="gallery-container">
        <ImageGallery images={images} onRemove={handleRemoveImage} />
      </div>
    </div>
  );
}

export default Annotator;
