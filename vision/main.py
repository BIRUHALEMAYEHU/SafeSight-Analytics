from fastapi import FastAPI, UploadFile, File
from deepface import DeepFace
import numpy as np
import cv2
import os

app = FastAPI()

os.environ["DEEPFACE_HOME"] = './model'

@app.post("/analyze")
async def analyze_frame(file: UploadFile = File(...)):
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    model_name = "SFace"
    CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR)
    PATH = os.path.join(PROJECT_ROOT, "known_faces")

    try:
        results = DeepFace.find(
            img_path=rgb_frame, 
            db_path=PATH, 
            enforce_detection=False, 
            silent=True,
            model_name=model_name,
            align=True
        )
        
        detections = []
        
        for df in results:
            if not df.empty:
                row = df.iloc[0]
                
                if 'identity' in row:
                    identity_path = row['identity']
                    
                    name = os.path.basename(os.path.dirname(identity_path))

                    detections.append({
                        "name": name,
                        "x": int(row.get('source_x', 0)),
                        "y": int(row.get('source_y', 0)),
                        "w": int(row.get('source_w', 0)),
                        "h": int(row.get('source_h', 0)),
                        "distance": float(row.get('distance', 0)) # Useful for debugging
                    })
        
        print(detections)
        return {"status": "success", "detections": detections}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)