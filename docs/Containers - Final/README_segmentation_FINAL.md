# 🧠 Segmentation Service – Visual Object Extractor

## 📌 Overview
The **Segmentation Service** is responsible for decomposing the uploaded user drawing into individual objects using **deep learning-based instance segmentation**. This is the first automated processing stage after image upload and plays a critical role in isolating visual elements for downstream analysis.

It supports two model types:
- `Detectron2` (Meta AI) – for high-accuracy segmentation.
- `YOLOv8-seg` (Ultralytics) – for faster, real-time segmentation.

---

## 🎯 Responsibilities

- Load a fine-tuned segmentation model (for sketch-like input).
- Perform instance segmentation on the uploaded image.
- Extract:
  - **Bounding boxes**
  - **Segmentation masks**
  - **Cropped object images**
- Generate `segmented_objects.json` with structured metadata per object.

---

## 🔄 Integration in System Workflow

| Stage        | Action |
|--------------|--------|
| Input        | Receives raw drawing image (`uploaded.png`) from backend |
| Processing   | Detects visual objects using pre-trained model |
| Output       | Cropped images per object + `segmented_objects.json` written to `shared/job_<uuid>/` |
| Next Step    | Feeds data into the **Object Processor** container |

---

## 🧠 Supported Algorithms: Detectron2 vs YOLOv8

| Feature     | Detectron2        | YOLOv8              |
|-------------|--------------------|---------------------|
| Developer   | Meta AI            | Ultralytics         |
| Strength    | High accuracy      | High speed          |
| Output      | Bounding boxes + masks | Same           |
| Framework   | PyTorch            | PyTorch             |
| Customization | Supports fine-tuning on sketch datasets | Supported |

Use can be toggled via config (`config.yaml`).

---

## ⚙️ Directory Structure

```
segmentation_service/
├── models/
│   └── model_weights.pth         # Pretrained weights (Detectron2 or YOLOv8)
├── utils/
│   ├── postprocessing.py         # Bounding box, mask cleanup, object sorting
│   └── visualizer.py             # Optional: overlay masks and labels
├── segment.py                    # Main segmentation script
├── config.yaml                   # Toggle model type and thresholds
└── requirements.txt
```

---

## 🧪 Sample Code – Detectron2

```python
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
import cv2

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = "models/model_weights.pth"
predictor = DefaultPredictor(cfg)

image = cv2.imread("shared/job_123/uploaded.png")
outputs = predictor(image)

instances = outputs["instances"]
masks = instances.pred_masks.cpu().numpy()
boxes = instances.pred_boxes.tensor.cpu().numpy()
```

---

## 🛠️ Post-Processing Steps

- Remove very small objects (noise filtering)
- Normalize bounding box coordinates (image-relative)
- Compute object center points (for distance)
- Export per-object crop to `objects/obj_<id>.png`
- Save `segmented_objects.json` with metadata

---

## 📄 Output Format – `segmented_objects.json`

```json
[
  {
    "object_id": "obj_001",
    "bounding_box": [120, 85, 240, 220],
    "mask": "<base64-encoded binary mask>",
    "center": [180, 152],
    "area": 3450,
    "cropped_image_path": "objects/obj_001.png"
  },
  {
    "object_id": "obj_002",
    "bounding_box": [260, 90, 400, 250],
    "mask": "<base64-encoded binary mask>",
    "center": [330, 170],
    "area": 5120,
    "cropped_image_path": "objects/obj_002.png"
  }
]
```

---

## 🔍 Edge Case Handling

| Scenario           | Behavior                                      |
|--------------------|-----------------------------------------------|
| No objects detected | Return empty list + log warning              |
| Clutter / scribbles | Filter by area + confidence threshold         |
| Heavy overlap       | Use instance-aware masking                    |
| Corrupted image     | Return 422 error or fail early                |

---

## 🧾 Dev Execution (Manual)

```bash
python segment.py --input shared/job_123/uploaded.png
```

- Outputs: `segmented_objects.json` + cropped PNGs.
- Logs saved to: `shared/job_123/log.txt`.

---

## 🔮 Future Improvements

- Integrate automatic fallback between Detectron2 and YOLOv8
- Add visual preview of segmentation via `visualizer.py`
- Train a custom model on abstract/child-drawing datasets
- Export segmentation masks as transparent PNGs for UI overlay

---

## 📌 Notes

- GPU inference (CUDA) strongly recommended.
- OpenCV is used internally for:
  - Cropping image based on mask
  - Area and contour-based filtering
- JSON output is passed directly to the **Object Processor** container.