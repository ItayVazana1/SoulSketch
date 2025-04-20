# 🧪 Object Processor – Feature Extractor with CNN & Color Analysis

## 📌 Overview
The **Object Processor** receives segmented object crops and performs visual analysis on each. It classifies object types using a **Quick, Draw!-trained CNN**, extracts **dominant colors**, maps them to psychological color categories, and outputs a structured JSON per object with enriched visual features.

This container is critical for preparing each object for relational scoring and psychological interpretation in the next stages.

---

## 🎯 Responsibilities

- Load and preprocess each cropped object image.
- Classify using a CNN trained on a subset of child-related Quick, Draw! categories (up to 20).
- Extract dominant RGB/HEX colors using K-means clustering (K=3).
- Map extracted colors to one of 9 predefined psychological categories using KNN.
- Compute basic features such as size and position.
- Export `object_features.json` with an entry for each object.

---

## 🔄 Integration in System Workflow

| Stage        | Action |
|--------------|--------|
| Input        | Cropped object PNGs + `segmented_objects.json` |
| Processing   | CNN classification + color clustering + emotion color mapping |
| Output       | Writes `object_features.json` to `shared/job_<uuid>/` |
| Next Step    | Data is passed to the **Comparator Engine** |

---

## 🧠 CNN Classifier Details

- **Dataset**: Subset of Google's Quick, Draw! (limited to 20 categories relevant to children’s sketches)
- **Model Architecture**: Custom CNN
  - 3 convolutional layers + max-pooling
  - Dense classification head
- **Input**: 28×28 or 64×64 grayscale image
- **Training**:
  - Data Augmentation: rotation, flip, noise
  - Optimizer: Adam
  - Target: ≥90% validation accuracy

---

## 🎨 Color Detection & Mapping Logic

### 1. **Dominant Color Extraction (KMeans)**
- Uses `KMeans(n_clusters=3)` on non-background RGB pixels.
- Filters out white/transparent pixels.
- Converts centroids to HEX format.
- Sorted by cluster size (dominance order).

### 2. **Color Mapping to Emotion Categories (KNN)**
Each extracted color is matched to one of **9 predefined color groups**:

| Color Group | Representative HEX | Emotion               |
|-------------|--------------------|------------------------|
| Yellow      | `#FFFF00`          | Warmth, Optimism       |
| Red         | `#FF0000`          | Energy, Aggression     |
| Blue        | `#0000FF`          | Calm, Sadness          |
| Green       | `#008000`          | Balance, Nature        |
| Black       | `#000000`          | Heaviness, Fear        |
| White       | `#FFFFFF`          | Purity, Emptiness      |
| Pink        | `#FFC0CB`          | Care, Softness         |
| Purple      | `#800080`          | Imagination, Fantasy   |
| Brown       | `#A52A2A`          | Grounding, Simplicity  |

A **KNN classifier (k=1)** is used in RGB space to assign each extracted color to the closest defined color category. The result is included as `mapped_emotional_colors` in the output JSON.

---

## 📁 Directory Structure

```
object_processor/
├── model/
│   ├── quickdraw_cnn.pt         # Trained CNN weights
│   └── class_labels.json        # Label → name mapping
├── analysis/
│   ├── color_extractor.py       # KMeans + color filtering
│   ├── color_mapper.py          # KNN color-to-emotion mapping
│   ├── classifier.py            # Torch CNN wrapper
│   └── object_builder.py        # Builds final feature JSON per object
├── object_processor.py          # Main execution script
└── requirements.txt
```

---

## 🧾 Output Format – `object_features.json`

```json
[
  {
    "object_id": "obj_001",
    "predicted_label": "sun",
    "dominant_colors": ["#FFD700", "#FF8C00", "#FFA500"],
    "mapped_emotional_colors": ["yellow", "orange", "orange"],
    "size": 3450,
    "position": { "x": 180, "y": 152 },
    "cropped_image_path": "objects/obj_001.png"
  }
]
```

---

## 🔍 Sample CNN Inference Code

```python
import torch
from torchvision import transforms
from PIL import Image
from model.quickdraw_cnn import MyCNNModel

model = MyCNNModel()
model.load_state_dict(torch.load("model/quickdraw_cnn.pt"))
model.eval()

img = Image.open("objects/obj_001.png").convert("L")
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])
input_tensor = transform(img).unsqueeze(0)

with torch.no_grad():
    logits = model(input_tensor)
    prediction = torch.argmax(logits, dim=1).item()
```

---

## 🔍 Edge Case Handling

| Scenario            | Behavior                      |
|---------------------|-------------------------------|
| Blank object        | Label = `"unknown"`           |
| Very small object   | Skip and log warning          |
| Model inference error | Fallback to default or "unknown" |
| Failed clustering   | Return `["#000000"]` or empty list |

---

## 🧪 Dev Execution (Manual)

```bash
python object_processor.py --job_id 123
```

- Reads: `segmented_objects.json`, cropped images.
- Writes: `object_features.json`
- Logs to: `shared/job_123/log.txt`

---

## 🔮 Future Enhancements

- Add classification confidence scores
- Export annotated thumbnails
- Use perceptual color distance (e.g., CIELAB) in color mapping
- Extend KNN to handle ambiguous colors (multi-label support)

---

## 📌 Notes

- **OpenCV** used for image loading, cropping, and resizing.
- **Pillow** handles format conversions.
- Output is used by the **Comparator Engine** in the next step.