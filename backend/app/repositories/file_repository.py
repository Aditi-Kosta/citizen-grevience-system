from pathlib import Path
import json
from typing import Any

class JsonRepository:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write([])

    def read(self) -> Any:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, value: Any) -> None:
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, ensure_ascii=False)
        temp.replace(self.path)

    def append(self, item: Any) -> None:
        data = self.read()
        data.append(item)
        self.write(data)
