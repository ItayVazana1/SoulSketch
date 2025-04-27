
# 🧠 Segmentation Service – SoulSketch Project

---

# 👁️ Overview

The **Segmentation Service** is the first core processing container of the **SoulSketch** system.  
It automatically detects and extracts individual objects from a user-uploaded drawing using YOLO-based instance segmentation models.

It prepares high-quality object crops for emotional analysis downstream.

- Supports multiple YOLO generations (**YOLOv8**, **YOLOv11**, **YOLOv12**).
- Designed for continuous, autonomous operation.

---

# 🔄 Full Flow (End-to-End)

| Step | Description |
|:-----|:------------|
| 1. Start | Service loads config.yaml and prepares environment |
| 2. Load Models | YOLO models (nano/small/medium) are loaded into memory |
| 3. Detect Job | Monitors `shared/` for latest `job_<uuid>` folder |
| 4. Wait for Upload | Waits for a valid uploaded image inside the job folder |
| 5. Image Inference | Runs all YOLO models on the image to extract bounding boxes |
| 6. Aggregate Detections | Collects all detections from all models |
| 7. Filter Duplicates | Uses IoU to remove overlapping bounding boxes |
| 8. Save Crops | Crops objects and saves them in the job folder |
| 9. Loop | Service continues to monitor for the next new job |

---

# 📊 Module Responsibilities

| File | Purpose | Main Functions |
|:-----|:--------|:---------------|
| `model_loader.py` | Load YOLO models | `load_models()` |
| `image_utils.py` | Load and save images | `load_image()`, `save_image()` |
| `crop_saver.py` | Save cropped images | `save_crops()`, `save_crop_from_bbox()` |
| `iou_utils.py` | Calculate IoU, remove duplicates | `calculate_iou()`, `filter_duplicates()` |
| `scorer.py` | (Optional) Score segmentation quality | `score_segmentation()` |
| `segmentor.py` | Extract bboxes or masks | `segment_image()`, `extract_bboxes()` |
| `segment_service.py` | Main service orchestrator | `run_segmentation_service()` |

---

# 📂 Folder Structure

```
segmentation_service/
├── models/
│   └── (YOLO weights organized)
├── utils/
│   ├── model_loader.py
│   ├── image_utils.py
│   ├── crop_saver.py
│   ├── iou_utils.py
│   ├── scorer.py
│   └── segmentor.py
├── segment_service.py
├── config.yaml
└── requirements.txt
```

---

# 📅 Configuration (`config.yaml`)

| Key | Purpose | Default |
|:----|:--------|:--------|
| `base_shared_dir` | Base folder for job_<uuid> | `../shared` |
| `check_interval_seconds` | Poll interval for uploaded files | `5` |
| `confidence_threshold` | YOLO detection threshold | `0.075` |
| `iou_threshold` | IoU threshold for duplicate removal | `0.4` |
| `models_dir` | Directory for YOLO weights | `./models` |
| `output_subdir` | Output folder name | `objects` |

---

# 🔧 Special Design Features

- **Multi-Model Aggregation**: Runs v8, v11, v12 models together.
- **Bounding Boxes Only**: Uses bboxes for simplicity and speed.
- **Duplicate Filtering**: IoU-based removal of overlapping detections.
- **Resilient Runtime**: Errors are logged and service retries after 5 seconds.
- **Systematic Naming**: Crops saved as `obj_<index>_<model_tag>.png`.

---

# 📚 External Python Libraries Used

| Package | Purpose |
|:--------|:--------|
| `ultralytics` | YOLO model management and inference |
| `opencv-python` | Image loading, manipulation |
| `numpy` | Efficient numerical operations |
| `PyYAML` | Load config.yaml |

### requirements.txt
```text
ultralytics>=8.0.0
opencv-python>=4.5.0
numpy>=1.19.0
PyYAML>=5.4.1
```

---

# 🤝 Future Improvements

- Add scoring logic to select best model dynamically.
- Support mask-based segmentation fallback.
- Add model ensemble voting (intersection of multiple models).
- Move from polling to messaging system (e.g., Redis queue).

---

# ✅ Conclusion

> **The Segmentation Service is a resilient, high-coverage pre-processing module that ensures accurate decomposition of children's drawings into meaningful objects, enabling downstream emotional analysis.**
