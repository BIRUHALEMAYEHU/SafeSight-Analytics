"""
SafeSight Analytics - Vision Service
Handles camera/video input and frame processing
"""

import cv2
import sys


def main():
    """Main function to read video frames from webcam or video file"""
    print("SafeSight Vision Service - Starting...")
    
    # Try to open webcam (camera index 0)
    cap = cv2.VideoCapture(0)
    
    # If webcam fails, try to open a sample video file
    if not cap.isOpened():
        print("Webcam not available, trying sample video file...")
        # You can specify a video file path here if needed
        # cap = cv2.VideoCapture("sample_video.mp4")
        print("No video source available. Please connect a webcam or provide a video file.")
        sys.exit(1)
    
    print("Video source opened successfully")
    print("Reading frames... (Press 'q' to quit)")
    
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to read frame or end of video reached")
                break
            
            frame_count += 1
            print(f"Frame {frame_count} received")
            
            # Optional: Display the frame (comment out if running headless)
            # cv2.imshow('SafeSight Vision', frame)
            
            # Optional: Break on 'q' key press (only works if imshow is enabled)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        cap.release()
        # cv2.destroyAllWindows()  # Uncomment if using imshow
        print(f"Stopped. Total frames processed: {frame_count}")


if __name__ == "__main__":
    main()

