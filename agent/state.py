from __future__ import __annotations__
from typing import Optional, TypedDict

class AgentState(TypedDict, total=False):
    prompt : str
    command : str
    explaination : str
    is_safe : bool
    safety_reason : bool
    stdout: bool
    stderr: bool
    executed: bool
    exit_code: Optional[int]


    

    
