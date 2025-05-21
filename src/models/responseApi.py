from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ResponseWrapper:
    data: Optional[Any] = None
    success: bool = True
    message: str = ""

    def to_dict(self):
        return {
            "data": self.data,
            "success": self.success,
            "message": self.message
        }