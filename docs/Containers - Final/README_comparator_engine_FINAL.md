# 📏 Comparator Engine – Relational Scoring Module

## 📌 Overview
The **Comparator Engine** is responsible for computing **relative feature scores** for each object in a drawing, placing it in the context of all other objects. Instead of evaluating an object’s absolute size or complexity, it determines how **unusual or extreme** its properties are within the specific drawing.

This context-aware scoring enables more meaningful emotion mapping downstream.

---

## 🎯 Responsibilities

- Load enriched object features from `object_features.json`.
- Compute the following for the full object set:
  - `average_size`
  - `average_distance_between_objects`
  - `average_complexity`
- For each object, calculate:
  - `relative_size_score`
  - `relative_distance_score`
  - `relative_complexity_score`
- Export `enriched_objects.json` with updated scores.

---

## 🔄 Integration in System Workflow

| Stage        | Action |
|--------------|--------|
| Input        | `object_features.json` from the Object Processor |
| Processing   | Calculate relational scores |
| Output       | Writes `enriched_objects.json` to `shared/job_<uuid>/` |
| Next Step    | Data is passed to the **Emotion Mapper** |

---

## 🧮 Scoring Logic Explained

### 1. 📐 Relative Size Score
- Formula: `relative_size_score = object_size / average_size`
- Indicates whether the object is larger (>1.0) or smaller (<1.0) than average.
- **Scale:**
  - 0.3–0.7 → Small
  - 0.7–1.3 → Normal
  - >1.3 → Large

---

### 2. 📏 Relative Distance Score
- For each object:
  - Compute its average distance to all other objects using Euclidean distance from object centers.
- Normalize the result by dividing by the global average.
- Formula: `relative_distance_score = avg_dist_from_obj / avg_pairwise_distance`
- **Scale:**
  - <0.7 → Close proximity
  - 0.7–1.3 → Normal spread
  - >1.3 → Isolated

---

### 3. 🧠 Relative Complexity Score
- Assumes each object has a `complexity_score` (e.g., from contour count, edge noise).
- Formula: `relative_complexity_score = complexity / average_complexity`
- **Scale:**
  - <0.7 → Simple
  - 0.7–1.3 → Normal
  - >1.3 → Complex

---

## 🧾 Example Output – `enriched_objects.json`

```json
[
  {
    "object_id": "obj_001",
    "predicted_label": "tree",
    "size": 3445,
    "position": { "x": 140, "y": 220 },
    "complexity_score": 0.62,
    "relative_size_score": 1.12,
    "relative_distance_score": 0.83,
    "relative_complexity_score": 0.94
  },
  {
    "object_id": "obj_002",
    "predicted_label": "person",
    "size": 2800,
    "position": { "x": 420, "y": 120 },
    "complexity_score": 0.41,
    "relative_size_score": 0.91,
    "relative_distance_score": 1.52,
    "relative_complexity_score": 0.63
  }
]
```

---

## 📁 Directory Structure

```
comparator_engine/
├── comparators/
│   ├── size.py              # Handles relative size calculation
│   ├── distance.py          # Computes distance matrix and normalization
│   ├── complexity.py        # Normalizes complexity across objects
├── scorer.py                # Coordinates all scoring logic
├── comparator_engine.py     # Main script
└── requirements.txt
```

---

## 🔍 Core Calculation Snippet

```python
# Relative size
avg_size = sum(obj["size"] for obj in objects) / len(objects)
for obj in objects:
    obj["relative_size_score"] = obj["size"] / avg_size

# Relative distance
def euclidean(a, b):
    return ((a["x"] - b["x"])**2 + (a["y"] - b["y"])**2) ** 0.5

for obj in objects:
    total_dist = sum(euclidean(obj["position"], other["position"]) for other in objects if obj != other)
    obj["relative_distance_score"] = total_dist / (len(objects) - 1)

# Normalize distance
mean_dist = sum(obj["relative_distance_score"] for obj in objects) / len(objects)
for obj in objects:
    obj["relative_distance_score"] /= mean_dist

# Relative complexity
avg_complexity = sum(obj["complexity_score"] for obj in objects) / len(objects)
for obj in objects:
    obj["relative_complexity_score"] = obj["complexity_score"] / avg_complexity
```

---

## 🔍 Edge Case Handling

| Scenario           | Behavior                                  |
|--------------------|-------------------------------------------|
| Only one object    | All scores default to `1.0`               |
| Missing attributes | Skip that object for that score           |
| Extreme outliers   | Optionally capped using quantile threshold |
| Non-numeric values | Logged and skipped                        |

---

## 🧪 Dev Execution (Manual)

```bash
python comparator_engine.py --job_id 123
```

- Reads: `object_features.json`
- Writes: `enriched_objects.json`
- Logs: `shared/job_123/log.txt`

---

## 🔬 Visual Debugging (Optional)

To validate the scores visually:
- Load the original drawing and overlay:
  - Object bounding boxes
  - Annotated scores (size, distance, complexity)
  - Color-coded scores (e.g., red = high, blue = low)

Use tools like `matplotlib` for rendering debugging overlays.

---

## 🔮 Future Enhancements

- Compute object-to-border distance (e.g., closeness to image edge)
- Detect object clusters or groups
- Weight scores by object importance
- Generate visual heatmaps per metric

---

## 📌 Notes

- All scores are **relative within the current drawing only**
- Output JSON is used by the **Emotion Mapper** to determine psychological meaning.