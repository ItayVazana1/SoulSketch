# 🛠️ SoulSketch – Development Specification Document

## 1. 🧠 Overview
SoulSketch is an interactive system for emotional analysis of drawings. It combines visual segmentation, object detection, color processing, comparative analysis, and emotion mapping based on psychological rules. The system is built as a set of modular containers working in sequence, with an accessible user interface and auto-generated summary reports.

---

## 2. 🔄 System Workflow (Step-by-Step)

1. **User uploads a drawing** via the UI
2. **Backend** receives the drawing, creates a job folder, and stores the image (`uploaded.png`)
3. **Segmentation Service** starts when `uploaded.png` appears – detects individual visual elements
4. **Object Processor** classifies each object (CNN), extracts dominant colors, and builds per-object JSONs
5. **Comparative Analysis (Comparator)**:
   - Calculates average size, distance, complexity
   - Assigns relative scores to each object
6. **Emotion Mapper**:
   - Applies rule-based psychological tagging
   - Adds `emotion_tag` to each object
7. **Backend (again)**:
   - Receives final JSON via `/analyze`
   - Generates a standardized PDF summary
8. **UI – Output to User**:
   - Displays analysis summary
   - Provides download link for PDF report

---

## 3. 🧩 System Architecture (Containers)

| Component | Role |
|-----------|------|
| **UI** | Upload drawing, display final analysis and PDF |

The graphical interface of the system will be developed using **Streamlit**, a Python-based framework for quickly building interactive web applications. Streamlit allows for easy integration of file uploads, progress updates, and result visualization, all without requiring JavaScript or CSS. The UI will interact with the backend using the `requests` library, and will be designed with a soft, accessible tone suitable for parents, educators, and psychologists.

| **Backend** | Handles both upload (stores drawing) and final output (PDF generation + API) |
| **Segmentation Service** | Extracts objects from the drawing via instance segmentation; uses OpenCV for cropping, masking, and mask-to-image conversions |
| **Object Processor** | Detects object type (CNN), extracts dominant colors; uses OpenCV for contour extraction, area calculation, and preprocessing filters |
| **Comparator Engine** | Computes relational metrics between objects |
| **Emotion Mapper** | Applies emotion tags based on visual psychology rules |

---

## 4. 📄 JSON File Structure (Partial Example)
```json
{
  "objects": [
    {
      "object_id": "obj_001",
      "predicted_label": "sun",
      "dominant_colors": ["#FFD700", "#FF8C00", "#FFA500"],
      "size": 3450,
      "position": { "x": 180, "y": 152 },
      "complexity_score": 0.72,
      "relative_size_score": 0.85,
      "relative_distance_score": 0.44,
      "emotion_tag": "warmth"
    }
  ]
}
```

---

## 5. ⚠️ Key Challenges & Solutions

| Challenge | Proposed Solution |
|----------|-------------------|
| Accurate segmentation of non-realistic drawings | Use Detectron2 or YOLOv8 with sketch-based fine-tuning |
| Object detection across varied styles | Limit to common QuickDraw-style classes, add fallback “unknown” |
| Measuring visual complexity | Define metrics like contour count, pixel density, edge noise |
| Ambiguity in emotion mapping | Use layered rule matching with confidence tiers |
| Integrating components | Shared volume per job, consistent JSON schema, REST API for final stage |

---

## 6. 🧾 Final Output
- A complete JSON file with object-level data and emotional tags
- A graphical PDF report summarizing the drawing and insights

---

## 7. ⏱️ Estimated Processing Time Per Container

| Container | Estimated Duration |
|-----------|--------------------|
| Segmentation Service | 15–30 seconds depending on drawing complexity |
| Object Processor | ~1–2 seconds per object |
| Comparator Engine | < 1 second (across all objects) |
| Emotion Mapper | < 1 second (rule-based logic) |
| Backend (PDF generation) | 1–3 seconds (Jinja2 + wkhtmltopdf) |

---

## 8. 🚨 Error Handling Strategy

- Each container logs to `shared/job_<uuid>/log.txt`
- If no objects detected → skip analysis, notify user
- If file missing or corrupt → return 422 error or fail early
- Timeouts: if a step exceeds 90 seconds, trigger fallback or log error
- Use default "unknown" labels for undefined classifications

---

## 9. 🧪 Running Containers (Development Mode)

Each container can be executed manually in development:

```bash
python segment.py --input shared/job_123/uploaded.png
python object_processor.py --job_id 123
python comparator_engine.py --job_id 123
python emotion_mapper_main.py --job_id 123
```

- Use `.env.dev` or CLI args for shared path overrides
- Logs written to `shared/job_<uuid>/log.txt`
- Outputs are always JSON files written to respective job folder

---

## 10. 🧭 Future Scalability Ideas

- Add container health checks + watchdog monitoring
- Introduce parallel processing where applicable
- Deploy model-based tagging fallback for missing rule matches

---

## 11. 🧰 Project Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit, Requests |
| **Backend** | Python, FastAPI, Jinja2, wkhtmltopdf |
| **Segmentation** | Detectron2 / YOLOv8, OpenCV, PyTorch |
| **Object Classification** | PyTorch, QuickDraw-trained CNN |
| **Color Analysis** | scikit-learn (KMeans), PIL |
| **Containerization** | Docker, Docker Compose |
| **Storage** | Shared file system (`shared/job_<uuid>/`), static file handling via backend |
| **Export** | PDF with embedded analysis using HTML template rendering |