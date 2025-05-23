import React, { useEffect, useState } from 'react';
import axiosInstance from '../../axiosInstance';
import './HomePage.css';

const HomePage = () => {
  const [images, setImages] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [replaceTarget, setReplaceTarget] = useState(null);
  const [search, setSearch] = useState('');
  const [previewImage, setPreviewImage] = useState(null);

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async (query = '') => {
    try {
      const res = await axiosInstance.get('/view', {
        params: { search: query }
      });
      setImages(res.data);
    } catch {
      alert('Failed to load images');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert('Select a file first.');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      if (replaceTarget) {
        formData.append('old_filename', replaceTarget);
        await axiosInstance.put('/replace', formData);
        alert('File replaced');
      } else {
        await axiosInstance.post('/upload', formData);
        alert('File uploaded');
      }

      setSelectedFile(null);
      setReplaceTarget(null);
      fetchImages();
    } catch (err) {
      alert(err?.response?.data?.message || 'Upload failed');
    }
  };

  const handleDownload = async (filename) => {
    try {
      const response = await axiosInstance.get(`/download/${filename}`, {
        responseType: 'blob', // Important for binary data
      });

      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));

      // Create a temporary <a> element to trigger download
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename); // Set default filename
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Download failed');
    }
  };

  const handleDelete = async (filename) => {
    try {
      await axiosInstance.delete('/delete', { data: { filename } });
      alert('Deleted successfully');
      setImages(images.filter(img => img.filename !== filename));
      if (replaceTarget === filename) setReplaceTarget(null);
    } catch (err) {
      alert(err?.response?.data?.message || 'Delete failed');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token'); 
    window.location.href = '/'; // redirect to login page
  };

  return (
    <div className="home-container">
      <h2>Image Manager</h2>
      <button className="btn logout-btn" onClick={handleLogout}>
        Logout
      </button>
      <input
        type="file"
        accept="image/*"
        onChange={e => setSelectedFile(e.target.files[0])}
        className="file-input"
      />

      {replaceTarget && <p className="replace-info">Replacing: {replaceTarget}</p>}

      <button className="btn upload-btn" onClick={handleUpload}>
        {replaceTarget ? 'Replace Image' : 'Upload Image'}
      </button>

      {replaceTarget && (
        <button
          className="btn cancel-btn"
          onClick={() => {
            setReplaceTarget(null);
            setSelectedFile(null);
          }}
        >
          Cancel Replace
        </button>
      )}

      <br /><br />
      <input
        type="text"
        placeholder="Search by filename"
        value={search}
        onChange={e => setSearch(e.target.value)}
        className="search-bar"
      />
      <button className="btn search-btn" onClick={() => fetchImages(search)}>
        Search
      </button>

      {previewImage && (
        <div className="preview-container">
          <div className="preview-overlay" onClick={() => setPreviewImage(null)} />
          <img src={previewImage} alt="Preview" className="preview-image" />
          <button className="btn close-btn" onClick={() => setPreviewImage(null)}>Close</button>
        </div>
      )}

      <div className="image-grid">
        {images.map(img => (
          <div key={img.filename} className="image-card">
            <div
              className="filename-only"
              onClick={() => setPreviewImage(`http://localhost:5000/uploads/${img.filename}`)}
              style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
            >
              {img.filename}
            </div>
            <button className="btn delete-btn" onClick={() => handleDelete(img.filename)}>
              Delete
            </button>
            <button className="btn replace-btn" onClick={() => setReplaceTarget(img.filename)}>
              Replace
            </button>
            <button className="btn download-btn" onClick={() => handleDownload(img.filename)}>
              Download
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
