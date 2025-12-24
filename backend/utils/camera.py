import cv2
import time
# from deepface import DeepFace # Moving to Vision Service
import os

class VideoCamera:
    def __init__(self, source=0):
        # source can be integer (webcam index) or string (RTSP URL or video file)
        self.video = cv2.VideoCapture(source)
        self.known_faces_db = "known_faces"
        self.current_name = "Scanning..."
        self.frame_count = 0
        self.face_detections = [] 
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            # If reading failed (e.g., end of video), reset if it's a file or return None
            return None
        
        self.frame_count += 1
        
        # DeepFace logic commented out for Phase 2 Refactoring
        # Logic will be moved to separate Vision Service
        """
        if self.frame_count % 10 == 0:
            try:
                # 'find' looks through the folder and matches the face
                results = DeepFace.find(img_path=frame, 
                                        db_path=self.known_faces_db, 
                                        model_name='VGG-Face', 
                                        enforce_detection=False,
                                        detector_backend='opencv')
                
                self.face_detections = []

                for df in results:
                    if not df.empty:
                        row = df.iloc[0]
                        full_path = row['identity']
                        name = os.path.basename(os.path.dirname(full_path)) 
                        
                        self.face_detections.append({
                            "name": name,
                            "x": int(row['source_x']),
                            "y": int(row['source_y']),
                            "w": int(row['source_w']),
                            "h": int(row['source_h'])
                        })
            except Exception as e:
                print(f"Matching error: {e}")
                self.current_name = "No Face"
        """
        
        # Mirror effect only for local webcam (source 0)
        # frame = cv2.flip(frame, 1) # Optional, depends on camera

        # Draw placeholders for detections (to be populated by Vision Service results in future)
        for face in self.face_detections:
            x, y, w, h = face['x'], face['y'], face['w'], face['h']
            name = face['name']

            # Draw the Bounding Box (Green)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y - 35), (x + w, y), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x + 6, y - 6), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.putText(frame, f"SafeSight: {time.strftime('%H:%M:%S')}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()