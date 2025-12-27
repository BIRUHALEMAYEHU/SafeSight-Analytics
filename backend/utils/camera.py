import httpx
import asyncio
import cv2
import time
import os

class VideoCamera:
    def __init__(self, source=0):
        self.video = cv2.VideoCapture(source)
        self.vision_url = "http://localhost:8001/analyze" 
        self.frame_count = 0
        self.face_detections = [] 
        self.is_processing = False
        
    def stop(self):
        """Properly release the camera"""
        if self.video.isOpened():
            self.video.release()

    async def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None
        
        self.frame_count += 1
        frame = cv2.flip(frame, 1)

        if self.frame_count % 10 == 0 and not self.is_processing:
            asyncio.create_task(self.send_to_vision_service(frame))

        for face in self.face_detections:
            x, y, w, h = face['x'], face['y'], face['w'], face['h']
            name = face['name']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y - 35), (x + w, y), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x + 6, y - 6), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.putText(frame, f"SafeSight: {time.strftime('%H:%M:%S')}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    async def send_to_vision_service(self, frame):
        """Sends the frame to the separate Vision Service API"""
        self.is_processing = True
        try:
            _, img_encoded = cv2.imencode('.jpg', frame)
            async with httpx.AsyncClient() as client:
                files = {'file': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')}
                response = await client.post(self.vision_url, files=files, timeout=5.0)
                
                if response.status_code == 200:
                    data = response.json()
                    self.face_detections = data.get("detections", [])
        except Exception as e:
            print(f"Vision Service Error: {e}")
        finally:
            self.is_processing = False