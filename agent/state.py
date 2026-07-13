from __future__ import annotations
from typing import Optional, TypedDict

class AgentState(TypedDict, total=False):
    prompt : str
    command : str
    explanation : str
    is_safe : bool
    safety_reason : str
    stdout: str
    stderr: str
    executed: bool
    exit_code: Optional[int]


    

    
