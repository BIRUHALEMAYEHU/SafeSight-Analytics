import httpx
import asyncio
import cv2
import time
import os
# from ultralytics import YOLO # Import the lightweight detection library - TEMPORARILY DISABLED

class VideoCamera:
    def __init__(self, source=0):
        self.video = cv2.VideoCapture(source)
        self.vision_url = "http://localhost:8001/analyze" 
        self.frame_count = 0
        self.face_detections = [] 
        self.is_processing = False
        
        # YOLO TEMPORARILY DISABLED - Uncomment when PyTorch DLL issue is resolved
        # print("Loading Object Detection Model...")
        # self.model = YOLO('yolov8n.pt') 
        # self.target_classes = [0, 2, 3, 5, 7]

    def stop(self):
        """Properly release the camera"""
        if self.video.isOpened():
            self.video.release()

    async def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None
        
        self.frame_count += 1
        # Flip frame (optional, depending on camera position)
        frame = cv2.flip(frame, 1)

        # --- GENERAL OBJECT DETECTION (Person/Car) --- TEMPORARILY DISABLED
        # results = self.model(frame, classes=self.target_classes, conf=0.4, verbose=False)
        # 
        # if not self.face_detections:
        #     for result in results:
        #         for box in result.boxes:
        #             x1, y1, x2, y2 = map(int, box.xyxy[0])
        #             cls = int(box.cls[0])
        #             
        #             color = (112, 128, 144) 
        #             
        #             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        #             
        #             label = self.model.names[cls] # e.g., 'person', 'car'
        #             (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        #             cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
        #             cv2.putText(frame, label.upper(), (x1, y1 - 5), 
        #                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        
        if self.frame_count % 10 == 0 and not self.is_processing:
            asyncio.create_task(self.send_to_vision_service(frame))

        # Draw Green Boxes for Identified Faces (from API)
        for face in self.face_detections:
            if all(k in face for k in ("x", "y", "w", "h")):
                x, y, w, h = face['x'], face['y'], face['w'], face['h']
                name = face.get("name", "Match")

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Name tag
                cv2.rectangle(frame, (x, y - 35), (x + w, y), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x + 6, y - 6), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # --- OVERLAYS ---
        # Timestamp(optional)
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