from fastapi import FastAPI, UploadFile, File
from deepface import DeepFace
import numpy as np
import cv2
import io

app = FastAPI()


@app.post("/analyze")
async def analyze_frame(file: UploadFile = File(...)):
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    model_name = "SFace"

    # perform matching
    try:
        results = DeepFace.find(img_path=frame, db_path="./known_faces", # these will be changed into 
                                enforce_detection=False, silent=True,model_name=model_name)
        
        detections = []
        for df in results:
            if not df.empty:
                row = df.iloc[0]
                detections.append({
                    "name": row['identity'].split('/')[-2], # these will be changed to the name wanted to identify 
                    "x": int(row['source_x']),
                    "y": int(row['source_y']),
                    "w": int(row['source_w']),
                    "h": int(row['source_h'])
                })
        return {"status": "success", "detections": detections}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 