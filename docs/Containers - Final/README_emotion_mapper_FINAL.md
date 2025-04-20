# 💡 Emotion Mapper – Rule-Based Psychological Tagging

## 📌 Overview
The **Emotion Mapper** is the final interpretation layer in the SoulSketch system. It analyzes enriched object features and applies **psychologically motivated rules** to assign each object an emotional tag.

This process enables the system to extract **symbolic and emotional meaning** from visual representations in children's drawings.

---

## 🎯 Responsibilities

- Load `enriched_objects.json` from the Comparator Engine.
- Analyze each object’s features:
  - Label (semantic meaning)
  - Dominant colors (RGB & mapped category)
  - Relative scores (size, distance, complexity)
- Apply a rule-based engine to assign:
  - `emotion_tag`
  - `rule_match_explanation`
- Output: `final_objects.json`

---

## 🔄 Integration in System Workflow

| Stage        | Action |
|--------------|--------|
| Input        | `enriched_objects.json` |
| Processing   | Apply emotion-mapping rules |
| Output       | Writes `final_objects.json` to `shared/job_<uuid>/` |
| Next Step    | Data is sent to Backend for PDF generation and UI display |

---

## 🧠 Core Mapping Logic

The emotion tag is determined by matching combinations of:
- `predicted_label` (object type)
- `mapped_emotional_colors` (from KNN mapping)
- `relative_size_score` (compared to peers)
- `relative_distance_score` (position in drawing)
- `relative_complexity_score` (visual density)

Each rule combines conditions on one or more fields and produces an emotion + explanation.

---

## 🎨 Emotional Color Mapping – 9 Categories

| Color | HEX      | Emotion |
|-------|----------|---------|
| Yellow | `#FFFF00` | Warmth, Optimism |
| Red    | `#FF0000` | Energy, Aggression |
| Blue   | `#0000FF` | Calm, Sadness |
| Green  | `#008000` | Nature, Balance |
| Black  | `#000000` | Fear, Heaviness |
| White  | `#FFFFFF` | Emptiness, Purity |
| Pink   | `#FFC0CB` | Care, Gentleness |
| Purple | `#800080` | Fantasy, Mystery |
| Brown  | `#A52A2A` | Simplicity, Grounding |

---

## 🧍 Recognized Object Labels – 20 Suggested

These were selected for high frequency and emotional relevance in children’s sketches:

1. Person  
2. Tree  
3. Sun  
4. House  
5. Heart  
6. Cloud  
7. Flower  
8. Car  
9. Bird  
10. Star  
11. Moon  
12. Animal  
13. Road  
14. Eye  
15. Hand  
16. Window  
17. Door  
18. Chair  
19. Mountain  
20. Balloon

---

## 📄 Output Format – `final_objects.json`

```json
[
  {
    "object_id": "obj_002",
    "predicted_label": "person",
    "dominant_colors": ["#A9A9A9", "#000000"],
    "mapped_emotional_colors": ["gray", "black"],
    "relative_size_score": 0.55,
    "relative_distance_score": 1.6,
    "relative_complexity_score": 0.9,
    "emotion_tag": "insecurity",
    "rule_match_explanation": "Small person placed far from others"
  }
]
```

---

## 🧩 File Structure

```
emotion_mapper/
├── rules/
│   └── mapping_rules.json       # All rules in JSON format
├── engine/
│   ├── rule_matcher.py          # Matching logic
│   └── emotion_mapper.py        # Main handler
├── emotion_mapper_main.py       # Entry script
└── requirements.txt
```

---

## 🛠️ Building Realistic Rules – A Practical Guide

Writing good psychological rules is **both art and science**. Here are key ideas to help you build a meaningful rule set:

### ✅ Anatomy of a Rule
Each rule should contain:
- **IF clause** – describes feature combinations
- **THEN clause** – defines the `emotion_tag` and rationale

```json
{
  "if": {
    "label": "person",
    "relative_size_score": { "lt": 0.6 },
    "relative_distance_score": { "gt": 1.3 }
  },
  "then": {
    "emotion_tag": "insecurity",
    "explanation": "Small person placed far from others"
  }
}
```

---

### 🧠 How to Start Crafting Rules:

1. **Start with intuition**:
   - "A small sun with black color → sadness"
   - "A big red heart → passion"

2. **Use known symbolism**:
   - Heart = affection, love
   - Tree = growth, stability
   - Black = fear or oppression

3. **Work with contrasts**:
   - If all objects are large and one is tiny → it’s “out of place”
   - If most are close together and one is far → it’s isolated

4. **Combine multiple signals**:
   - Don’t rely on label only – include size, distance, color

5. **Use safe defaults**:
   - If no strong features exist → tag as "neutral"

6. **Test and iterate**:
   - As you review more drawings, refine your rule set

---

### 💡 Example Rule Ideas:

| Situation | Rule |
|----------|------|
| Small person, far from group | `insecurity` |
| Tree far away, alone | `isolation` |
| Bright sun in center | `warmth` |
| Red star with high complexity | `intensity` |
| House in black | `fear of home` |
| Heart small and dark | `emotional withdrawal` |

---

## 🔍 Edge Case Handling

| Scenario              | Behavior                          |
|-----------------------|-----------------------------------|
| No rule matches       | Assign `"neutral"` or fallback    |
| Multiple rules match  | Select strongest match (first or weighted) |
| Missing attributes    | Skip rule, tag as `"undefined"`   |

---

## 🧪 Dev Execution (Manual)

```bash
python emotion_mapper_main.py --job_id 123
```

- Reads: `enriched_objects.json`
- Writes: `final_objects.json`
- Logs: `shared/job_123/log.txt`

---

## 🔮 Future Enhancements

- Admin UI to create, test and edit rules
- Introduce ML fallback (e.g., KNN) for rule gaps
- Rule scoring and priority weighting
- Group-level emotion analysis (emotion clusters in drawing)

---

## 📌 Notes

- Rules are stored in editable JSON files
- Color mapping must align with KNN used by Object Processor
- Final results are used for PDF generation and visual presentation