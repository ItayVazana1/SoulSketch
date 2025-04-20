# 📆 SoulSketch – Chronological TODO List with Timeline (Apr 20 – May 21)

This version of the TODO list is organized **by execution order**, and includes recommended **date ranges** for completing each part, based on a final available workday of **May 21** and project submission on **May 25**.

---

## 🟢 Week 1 (Apr 20–26) – Project Kickoff & Infrastructure

- [ ] Apr 20–21: ✅ Prepare full architecture & JSON format definitions
- [ ] Apr 21–22: Set up shared folder structure (`shared/job_<uuid>/`)
- [ ] Apr 22–23: Finalize mapping_rules.json (basic emotional rules)
- [ ] Apr 23–24: Create full project README + container READMEs
- [ ] Apr 25–26: Prepare `test_<module>.py` templates for each container

---

## 🧠 Week 2 (Apr 27–May 3) – Backend + Segmentation

- [ ] Apr 27–28: Implement `/upload`, `/status`, `/results/:id`, `/pdf/:id`
- [ ] Apr 29–30: Integrate Jinja2 + wkhtmltopdf for PDF rendering
- [ ] May 1–2: Implement segmentation (Detectron2 or YOLOv8 base)
- [ ] May 3: Generate `segmented_objects.json` + save object crops

---

## 🧪 Week 3 (May 4–10) – Object Processor + Comparator Engine

- [ ] May 4–5: CNN classification using QuickDraw-trained model
- [ ] May 5–6: Extract dominant colors (KMeans)
- [ ] May 6–7: Map colors to emotions (KNN)
- [ ] May 7–8: Write `object_features.json`
- [ ] May 9–10: Compute size/distance/complexity → `enriched_objects.json`

---

## 💡 Week 4 (May 11–15) – Emotion Mapper + Testing

- [ ] May 11–12: Implement rule matcher + load `mapping_rules.json`
- [ ] May 13: Apply rules per object → write `final_objects.json`
- [ ] May 14–15: Write test cases for all logic steps

---

## 🎨 Week 5 (May 16–20) – UI + Integration + Polish

- [ ] May 16–17: Build Streamlit UI (upload → status → results → PDF)
- [ ] May 18: Validate full system run (from image to PDF)
- [ ] May 19: UX polish + error messages + visual design
- [ ] May 20: Write final logics & verify edge cases

---

## 📤 May 21 (Final Workday)

- [ ] Run one complete job & generate all outputs (json + pdf)
- [ ] Create screenshots for submission poster/video
- [ ] Final system test (all modules together)

---

## 🧪 Bonus Tasks (if time permits)

- [ ] Add color-coded overlays to segmented output (visualizer.py)
- [ ] Improve CNN model confidence threshold
- [ ] Add fallback emotion tag logic (e.g., "undefined")

---

> ✅ Use this as your delivery roadmap – you're right on track to finish strong!
