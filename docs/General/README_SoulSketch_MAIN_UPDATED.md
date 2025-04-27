# 🧠 SoulSketch – Emotional Analysis of Children's Drawings

SoulSketch is a modular system for psychological interpretation of children’s drawings. It uses deep learning, color analysis, comparative reasoning, and rule-based inference to generate insights about emotional states, all packed into an intuitive user experience with downloadable reports.

---

## 🧩 System Overview

SoulSketch is composed of 6 key containers working together:

1. 🎨 **UI** – Frontend for upload, status tracking, result viewing, and PDF download
2. 🧩 **Backend** – Coordinates upload/init + final PDF/report generation and API exposure
3. 🧠 **Segmentation Service** – Performs object extraction from drawing using Detectron2 or YOLOv8
4. 🧪 **Object Processor** – Classifies each object with a CNN, extracts colors, maps to emotion categories
5. 📏 **Comparator Engine** – Computes object-relative size/distance/complexity scores
6. 💡 **Emotion Mapper** – Applies rule-based psychological tagging for each object

---

## 🔄 Processing Flow

1. **Upload** → UI sends drawing to backend via `/upload`
2. **Segmentation** → Extracts objects → `segmented_objects.json`
3. **Object Analysis** → CNN label + KMeans colors + KNN color emotion → `object_features.json`
4. **Relational Scoring** → `relative_*_score` → `enriched_objects.json`
5. **Emotion Mapping** → Rules applied → `final_objects.json`
6. **PDF Generation** → Backend creates final report and responds to UI

---

## 🧪 File Exchange Structure

```
shared/
└── job_<uuid>/
    ├── uploaded.png
    ├── segmented_objects.json
    ├── object_features.json
    ├── enriched_objects.json
    ├── final_objects.json
    └── report.pdf
```

---

## 🔌 Backend REST API

| Method | Route         | Description |
|--------|---------------|-------------|
| POST   | `/upload`     | Upload a drawing, return job ID |
| POST   | `/analyze`    | Submit final JSON for PDF |
| GET    | `/status/:id` | Check job status |
| GET    | `/results/:id`| Get emotion data + PDF link |
| GET    | `/pdf/:id`    | Download final PDF report |

---

## 🎨 Visual UI Design (Streamlit)

The user interface is implemented with **Streamlit**, allowing users to upload a drawing, monitor the progress of the analysis in real time, and view/download results. The interface uses built-in Streamlit components for uploads, layout, and interactivity, and communicates with the backend using the `requests` library.

- **Upload Section** – image file selection with preview
- **Processing Display** – loading message and backend status polling
- **Results Section** – object-level insights including color swatches and emotion tags
- **Download Button** – link to download the final PDF report

The design is clean and emotionally accessible, suitable for use by parents, psychologists, and educators.

---

## 🧠 Intelligence Modules Summary

### 1. **Segmentation** (Detectron2 / YOLOv8)
- Mask + bounding box detection
- Filters noise, saves cropped object images

### 2. **Object Processor**
- CNN classification from 20 QuickDraw labels
- KMeans (K=3) for dominant colors
- KNN mapping to 9 emotional color categories

### 3. **Comparator Engine**
- Computes 3 relational scores:
  - Relative Size
  - Relative Distance
  - Relative Complexity

### 4. **Emotion Mapper**
- Rules combine label + color + scores
- 20 object types supported
- 9 emotional colors
- Example rule: *"Small person far from group → insecurity"*

---

## 📄 Sample Final Output (`final_objects.json`)

```json
[
  {
    "object_id": "obj_002",
    "predicted_label": "person",
    "mapped_emotional_colors": ["black", "gray"],
    "relative_size_score": 0.55,
    "relative_distance_score": 1.6,
    "emotion_tag": "insecurity",
    "rule_match_explanation": "Small person placed far from others"
  }
]
```

---

## 📌 Tech Stack

| Layer        | Technology |
|--------------|------------|
| Frontend     | Streamlit, Requests |
| Backend/API  | FastAPI, Python |
| Segmentation | PyTorch, Detectron2 / YOLOv8, OpenCV |
| Classification | PyTorch CNN (QuickDraw) |
| Color Mapping | Scikit-learn (KMeans, KNN), PIL |
| Emotion Mapping | Custom JSON rule engine |
| PDF Export   | Jinja2 + wkhtmltopdf |
| Deployment   | Docker, Shared Volume FS |

---

## 🧪 Dev Mode – Manual Run

```bash
python segment_service.py --input shared/job_123/uploaded.png
python object_processor.py --job_id 123
python comparator_engine.py --job_id 123
python emotion_mapper_main.py --job_id 123
```

---

## 📊 Performance & Timing

| Container          | Duration     |
|--------------------|--------------|
| Segmentation       | 15–30s       |
| Object Processor   | 1–2s per obj |
| Comparator         | <1s total    |
| Emotion Mapper     | <1s total    |
| Backend (PDF)      | 1–3s         |

---

## 🚨 Error Handling

- Logs in: `shared/job_<uuid>/log.txt`
- Timeouts → fallback or skip
- No objects detected → warning
- Missing files → error response (422)

---

## 🔮 Future Additions

- ML fallback for emotion mapping
- Rule editor UI
- S3-like storage
- Role-based views (parent / teacher)
- Real-time drawing canvas (sketch to emotion live)

---

## 📎 Related Files

- `README_segmentation.md`
- `README_object_processor.md`
- `README_comparator_engine.md`
- `README_emotion_mapper.md`
- `README_backend.md`
- `README_UI.md`