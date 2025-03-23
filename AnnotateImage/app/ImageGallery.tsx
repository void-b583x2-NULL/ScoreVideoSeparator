import React, { useState } from 'react';

interface ImageGalleryProps {
  images: string[];
  onRemove: (imageToRemove: string) => void;
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ images, onRemove }) => {
  const [annotations, setAnnotations] = useState<{ [key: string]: number[] }>({});

  // Handle image click to add an annotation (horizontal line)
  const handleImageClick = (image: string, event: React.MouseEvent<HTMLImageElement>) => {
    const imageElement = event.target as HTMLImageElement;
    const rect = imageElement.getBoundingClientRect();
    const clickPosition = event.clientY - rect.top; // Calculate position relative to image container

    const imageId = image;

    setAnnotations((prevAnnotations) => {
      const newAnnotations = { ...prevAnnotations };
      if (!newAnnotations[imageId]) {
        newAnnotations[imageId] = [];
      }
      newAnnotations[imageId].push(clickPosition);
      return newAnnotations;
    });
  };

  // Handle undo functionality for the last added line
  const handleUndo = (image: string) => {
    setAnnotations((prevAnnotations) => {
      const newAnnotations = { ...prevAnnotations };
      if (newAnnotations[image]?.length > 0) {
        newAnnotations[image].pop(); // Remove the last annotation
      }
      return newAnnotations;
    });
  };

  return (
    <div className="gallery">
      {images.map((image, index) => (
        <div key={index} className="image-container">
          <img
            src={image}
            alt={`Image ${index}`}
            onClick={(event) => handleImageClick(image, event)}
            style={{ cursor: 'pointer' }}
          />
          <button
            className="remove-btn"
            onClick={() => onRemove(image)}
          >
            Remove
          </button>
          <button
            className="undo-btn"
            onClick={() => handleUndo(image)}
          >
            Undo Last Line
          </button>

          {/* Render the annotations (horizontal lines) */}
          <div className="annotations">
            {annotations[image]?.map((position, idx) => (
              <div
                key={idx}
                className="annotation-line"
                style={{ top: position - 1 }} // Slightly adjust the line position to center it
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImageGallery;
