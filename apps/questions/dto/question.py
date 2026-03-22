from dataclasses import dataclass
from typing import Optional


@dataclass
class ListQuestionsQuery:
    page: int = 1
    limit: int = 10
    category_id: Optional[int] = None
