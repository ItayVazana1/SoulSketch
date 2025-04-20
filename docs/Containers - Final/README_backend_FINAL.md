# 🧩 Backend – System Coordinator & Report Generator

## 📌 Overview
The **Backend** is the central coordinator in the SoulSketch system. It serves two major roles:

1. At the **start** – it accepts the uploaded drawing from the UI, generates a job ID, and stores the image in the shared volume.
2. At the **end** – it receives the final analyzed data, generates a downloadable PDF report, and serves the results back to the user interface.

It acts as the bridge between processing logic and user presentation.

---

## 🎯 Responsibilities

- Accept user uploads (`/upload`) and initialize job folders
- Store raw image and manage job UUIDs
- Accept final emotional analysis JSON (`/analyze`)
- Generate PDF report using HTML template and `wkhtmltopdf`
- Provide APIs for status checking and result retrieval
- Manage internal file storage and cleanup for expired jobs

---

## 🔄 System Integration Points

| Stage      | Role |
|------------|------|
| Initial    | Receives drawing → saves to `shared/job_<uuid>/uploaded.png` |
| Final      | Receives `final_objects.json` → generates `report.pdf` |
| Persistent | Exposes REST API for UI interaction |

---

## 🔌 REST API Specification

| Method | Route         | Description |
|--------|---------------|-------------|
| `POST` | `/upload`     | Upload drawing, receive `job_id` |
| `POST` | `/analyze`    | Submit final JSON for report generation |
| `GET`  | `/status/:id` | Check if job is still running, failed, or completed |
| `GET`  | `/results/:id`| Get emotional analysis JSON + PDF path |
| `GET`  | `/pdf/:id`    | Stream the final report (application/pdf) |

---

## 🧾 Output Format Example

### Example response from `/results/:id`:

```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "complete",
  "final_objects": [ ... ],
  "pdf_url": "/pdf/123e4567-e89b-12d3-a456-426614174000"
}
```

---

## 📄 Directory Structure

```
backend/
├── app/
│   ├── routes/
│   │   └── api.py              # All API endpoints
│   ├── services/
│   │   ├── storage.py          # JSON & PDF file I/O
│   │   ├── pdf_generator.py    # Uses Jinja2 + wkhtmltopdf
│   └── main.py                 # FastAPI entrypoint
├── templates/
│   └── report_template.html    # Jinja2 layout for PDF
├── static/                     # Stored PDFs & final JSONs
└── requirements.txt
```

---

## 🧠 PDF Generation Process

1. Loads `final_objects.json`
2. Populates an HTML template (`report_template.html`)
3. Renders using `wkhtmltopdf` to ensure consistent layout
4. Saves `report.pdf` to `shared/job_<uuid>/`

---

## 📌 Content in PDF

- Drawing metadata (name, upload time)
- List of detected objects with:
  - Label
  - Mapped emotional color(s)
  - Relative scores
  - Emotion tag + explanation
- Icons or symbolic color swatches (optional)

---

## 🔍 Edge Case Handling

| Case | Behavior |
|------|----------|
| Invalid JSON structure | Returns 422 + schema validation error |
| Missing job ID | Returns 404 with helpful message |
| PDF rendering failure | Returns 500 + logs error details |
| Job folder not found | Suggests re-uploading drawing |

---

## 🔒 Job ID & Security

- Job IDs are UUIDv4 – hard to guess
- Files are stored under `/shared/job_<uuid>/`
- Backend can clean up expired jobs periodically

---

## 🧪 Dev Execution (Manual)

```bash
uvicorn app.main:app --reload --port 8000
```

- Test `/upload` with image using Postman or `curl`
- Use `shared/` as a volume mount in Docker
- Logs stored per job in `shared/job_<uuid>/log.txt`

---

## 🔮 Future Improvements

- Add authentication for multi-user support
- Role-based access (parent / teacher / psychologist)
- Support multiple uploads per session
- Store job data in a lightweight DB
- Add visual PDF preview via HTML in UI

---

## 📌 Notes

- PDF generation uses `wkhtmltopdf` (requires system binary)
- Jinja2 handles data binding to HTML
- All API responses should be schema-validated with Pydantic