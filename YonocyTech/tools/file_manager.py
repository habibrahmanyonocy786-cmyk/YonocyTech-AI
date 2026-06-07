import os
from typing import List, Optional
from security.guard import is_code_safe

class FileManager:
    """
    Provides secure file system operations with extension restrictions.
    """
    ALLOWED_READ_EXTENSIONS = {".txt", ".py", ".md", ".csv", ".json", ".pdf", ".docx", ".xlsx"}
    ALLOWED_WRITE_EXTENSIONS = {".txt", ".py", ".md", ".csv", ".json"}

    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _safe_path(self, filename: str) -> str:
        # Prevent path traversal attacks
        clean_name = os.path.basename(filename)
        return os.path.join(self.base_dir, clean_name)

    def read(self, filename: str) -> Optional[str]:
        """
        Reads the content of a file if the extension is allowed.
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_READ_EXTENSIONS:
            return f"Error: File extension {ext} is not allowed for reading."

        path = self._safe_path(filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write(self, filename: str, content: str) -> bool:
        """
        Writes content to a file if the extension is allowed.
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_WRITE_EXTENSIONS:
            return False

        # Basic content safety check if it's a python file
        if ext == ".py":
            safe, pattern = is_code_safe(content)
            if not safe:
                return False

        path = self._safe_path(filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception:
            return False

    def list_dir(self) -> List[str]:
        """
        Lists all files in the base directory.
        """
        return os.listdir(self.base_dir)

    def delete(self, filename: str) -> bool:
        """
        Deletes a file from the base directory.
        """
        path = self._safe_path(filename)
        try:
            if os.path.exists(path):
                os.remove(path)
                return True
            return False
        except Exception:
            return False
