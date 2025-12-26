import httpx
import asyncio
import cv2

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.detections = []
        self.vision_url = "http://localhost:8001/analyze"
        self.is_processing = False

    async def get_frame(self):
        success, frame = self.video.read()
        if not success: return None

        
        if not self.is_processing:
            asyncio.create_task(self.send_to_vision_service(frame))
            
        for d in self.detections:
            cv2.rectangle(frame, (d['x'], d['y']), (d['x']+d['w'], d['y']+d['h']), (0, 255, 0), 2)
            cv2.putText(frame, d['name'], (d['x'], d['y']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    async def send_to_vision_service(self, frame):
        self.is_processing = True
        try:
            _, img_encoded = cv2.imencode('.jpg', frame)
            async with httpx.AsyncClient() as client:
                files = {'file': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')}
                response = await client.post(self.vision_url, files=files, timeout=None)
                if response.status_code == 200:
                    data = response.json()
                    self.detections = data.get("detections", [])
        except Exception as e:
            print(f"Vision Service unreachable: {e}")
        finally:
            self.is_processing = False