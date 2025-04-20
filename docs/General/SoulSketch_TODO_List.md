# ✅ SoulSketch Project – TODO Checklist (Container by Container)

This is a modular development checklist for the SoulSketch project. It outlines the required actions, file creation points, and expected outputs at each stage of the system.

---

## 🧠 Overview – Job Folder Lifecycle
```
shared/job_<uuid>/
├── uploaded.png
├── segmented_objects.json
├── object_features.json
├── enriched_objects.json
├── final_objects.json
└── report.pdf
```

---

## 🎨 UI – Streamlit Interface

- [ ] Upload drawing via `POST /upload`
- [ ] Poll job status via `GET /status/:job_id`
- [ ] Fetch analysis results via `GET /results/:job_id`
- [ ] Display final emotion tags + download button (`GET /pdf/:job_id`)

---

## 🧩 Backend

### Initial Stage
- [ ] Receive image via `/upload`
- [ ] Create `shared/job_<uuid>/uploaded.png`

### Final Stage
- [ ] Receive `final_objects.json` via `/analyze`
- [ ] Generate `report.pdf` using Jinja2 + wkhtmltopdf
- [ ] Serve results via REST API

---

## 🧠 Segmentation Service

- [ ] Wait for `uploaded.png` to appear
- [ ] Perform segmentation using Detectron2 or YOLOv8
- [ ] Save object crops to `objects/obj_<id>.png`
- [ ] Generate `segmented_objects.json`
- [ ] Log to `log.txt`

---

## 🧪 Object Processor

- [ ] Read `segmented_objects.json` and cropped images
- [ ] Classify each object using QuickDraw CNN
- [ ] Extract dominant colors via KMeans (K=3)
- [ ] Map each color to emotion using KNN
- [ ] Generate `object_features.json`
- [ ] Log to `log.txt`

---

## 📏 Comparator Engine

- [ ] Load `object_features.json`
- [ ] Compute:
  - [ ] `relative_size_score`
  - [ ] `relative_distance_score`
  - [ ] `relative_complexity_score`
- [ ] Output `enriched_objects.json`
- [ ] Log to `log.txt`

---

## 💡 Emotion Mapper

- [ ] Load `enriched_objects.json`
- [ ] Match against `mapping_rules.json`
- [ ] Add `emotion_tag` and `rule_match_explanation`
- [ ] Output `final_objects.json`
- [ ] Log to `log.txt`

---

## 🧪 Testing Scripts (per container)

- [ ] `test_segmentation.py`
- [ ] `test_object_processor.py`
- [ ] `test_comparator.py`
- [ ] `test_emotion_mapper.py`
- [ ] `test_backend.py`

---

## 📄 Dev Manual Run (Example Job 123)
```bash
python segment.py --input shared/job_123/uploaded.png
python object_processor.py --job_id 123
python comparator_engine.py --job_id 123
python emotion_mapper_main.py --job_id 123
```

---

## 🧹 Final Checks
- [ ] All logs written to `log.txt`
- [ ] All outputs use correct schema
- [ ] Every module runs standalone
- [ ] UI reflects emotional summary visually and clearly

---

> Tip: Use this list as a progress tracker for dev & testing. You can extend it with timing stats or additional dev notes per container.
