
const VideoStream = () => {
  return (
    <div className="video-container">
      <h2>Live Surveillance Feed</h2>
      <div style={{ border: '2px solid #333', borderRadius: '8px', overflow: 'hidden' }}>
        <img
          src="http://localhost:8000/video_feed"
          alt="Live Stream"
          style={{ width: '100%', maxWidth: '800px', display: 'block' }}
        />
      </div>
      <p>Status: <span style={{ color: 'green' }}>● Live</span></p>
    </div>
  );
};

export default VideoStream;