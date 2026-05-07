from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BorrowRecord:
    user_id: str
    book_id: str
    borrow_date: datetime
    expected_return_date: datetime
    actual_return_date: Optional[datetime] = None
    id: Optional[str] = None
