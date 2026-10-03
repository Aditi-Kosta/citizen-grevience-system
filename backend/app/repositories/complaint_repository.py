from pathlib import Path
import json
from typing import Optional
from backend.app.config import DATA_DIR

PATH = DATA_DIR / "demo" / "complaints.json"

class ComplaintRepository:
    def __init__(self, path: Path = PATH):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists(): self.path.write_text("[]", encoding="utf-8")

    def all(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, complaint_id: str):
        return next((x for x in self.all() if x["complaint_id"] == complaint_id), None)

    def save(self, item):
        rows = self.all()
        rows = [x for x in rows if x["complaint_id"] != item["complaint_id"]]
        rows.append(item)
        self.path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        return item

    def count(self): return len(self.all())

    def filter(self, department=None, category=None, urgency=None, status=None, cluster_id=None, q=None):
        rows = self.all()
        if department: rows = [x for x in rows if x.get("department") == department]
        if category: rows = [x for x in rows if x.get("category") == category]
        if urgency: rows = [x for x in rows if x.get("urgency") == urgency]
        if status: rows = [x for x in rows if x.get("status") == status]
        if cluster_id is not None: rows = [x for x in rows if x.get("cluster_id") == cluster_id]
        if q: rows = [x for x in rows if q.lower() in x.get("text", "").lower()]
        return rows
