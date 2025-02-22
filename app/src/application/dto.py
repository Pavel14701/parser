from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True)
class Filters:
    agency: Optional[str]
    address: Optional[str]
    
