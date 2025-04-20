# 🧱 SoulSketch – System Architecture Overview

## 1. 🧠 System Concept

SoulSketch is composed of 6 modular containers, each performing a distinct stage of the emotional analysis pipeline. The system is designed as a linear processing flow, where each container enriches the input and passes it to the next container, until the final emotional insights are presented back to the user.

There is no centralized scheduler or orchestrator – the execution order is deterministic and follows a simple "pass and process" model.

---

## 2. 🧩 Container Overview

| Container | Description |
|-----------|-------------|
| 🎨 UI | User-facing interface built with Streamlit for uploading a drawing, tracking progress, and viewing results |
| 🧩 Backend | Central processing server – receives input, routes files, exposes API, and generates report |
| 🧠 Segmentation Service | Performs instance segmentation and generates object crops |
| 🧪 Object Processor | Classifies object type (CNN), extracts dominant colors |
| 📏 Comparator Engine | Computes relational metrics (size, distance, complexity) |
| 💡 Emotion Mapper | Applies rule-based emotional interpretation |

---

## 3. 🔄 Data Flow Between Containers

| From → To | Format | Transport Method |
|-----------|--------|------------------|
| UI → Backend | Image file (.png or .jpg) | HTTP POST to `/upload` |
| Backend → Segmentation | Image path in shared volume | File path in `shared/job_<uuid>/uploaded.png` |
| Segmentation → Object Processor | Cropped images + segmented_objects.json | Shared folder + JSON |
| Object Processor → Comparator | object_features.json | Shared JSON file |
| Comparator → Emotion Mapper | enriched_objects.json | Shared JSON file |
| Emotion Mapper → Backend | final_objects.json | HTTP POST to `/analyze` |
| Backend → UI | PDF + JSON | HTTP API (GET `/results/:id`) |

---

## 4. 📄 Shared Object JSON Structure

Each container adds fields to the object-level JSON:

```json
{
  "object_id": "obj_003",
  "predicted_label": "house",
  "dominant_colors": ["#FFCC00", "#A52A2A"],
  "position": { "x": 250, "y": 170 },
  "size": 4200,
  "complexity_score": 1.12,
  "relative_size_score": 1.05,
  "relative_distance_score": 0.88,
  "relative_complexity_score": 1.07,
  "emotion_tag": "security"
}
```

---

## 5. 🔗 Execution Order

The processing flow is strictly sequential. Each container:
- Waits for specific file(s) in the shared directory
- Begins only after its dependencies are available
- Writes structured output for the next container

---

## 6. 📁 Shared Directory Structure

```
shared/
└── job_<uuid>/
    ├── uploaded.png                 # from UI via Backend
    ├── segmented_objects.json       # from Segmentation
    ├── object_features.json         # from Object Processor
    ├── enriched_objects.json        # from Comparator
    ├── final_objects.json           # from Emotion Mapper
    └── report.pdf                   # from Backend
```

---

## 7. 🕹️ Trigger Logic

| Container | Trigger | Reads | Writes |
|-----------|---------|-------|--------|
| Backend (initial) | `/upload` HTTP call | uploaded image | saved to `shared/job_<uuid>/uploaded.png` |
| Segmentation | uploaded.png exists | uploaded image | segmented_objects.json |
| Object Processor | segmented_objects.json exists | + object crops | object_features.json |
| Comparator | object_features.json exists | | enriched_objects.json |
| Emotion Mapper | enriched_objects.json exists | | final_objects.json |
| Backend (final) | `/analyze` is POSTed | final_objects.json | report.pdf |
| UI (final) | Polls `/results/:id` | PDF + summary | Displays output to user |

---

## 8. 🧪 Inter-Container File Exchange – Code Examples

```python
# Segmentation writes output
with open("shared/job_123/segmented_objects.json", "w") as f:
    json.dump(object_list, f)
```

```python
# Object Processor reads it
with open("shared/job_123/segmented_objects.json", "r") as f:
    objects = json.load(f)
```

```python
# Emotion Mapper sends final result to backend
requests.post("http://backend:8000/analyze", json=final_data)
```

---

## 9. 🧭 Future Scalability Ideas

- Introduce task orchestrator (e.g., Celery, Prefect)
- Support parallelization per object
- Move data handling to DB or object storage (e.g., S3)