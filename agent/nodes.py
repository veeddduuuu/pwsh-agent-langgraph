from __future__ import annotations
from sys import stdout
from .state import AgentState

from executor import run_command
from llm import generate_command
from safety import screen_command

def generate_command_node(state: AgentState) -> AgentState:
    command, explaination = generate_command(state["prompt"])

    return{
        "command":command,
        "explanation":explaination
    }

def screen_command_node(state: AgentState) -> AgentState:
    is_safe, reason = screen_command[state["command"]]
    return{
        "is_safe":is_safe,
        "safety_reason":reason
    }

def execute_command_node(state: AgentState) -> AgentState:
    if not state.get("is_safe", True):
        return{
            "executed":False,
            "stdout":"",
            "stderr":"The cmd was cancelled due to safety reasons"
            "exit_code":None
        }

    result = run_command(state["command"])
    return {
        "executed": True,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exit_code,
    }

def blocked_node(state: AgentState) -> AgentState:
    return {
        "executed": False,
        "stdout": "",
        "stderr": "Execution blocked by safety screen: "
        + state.get("safety_reason", "unknown reason"),
        "exit_code": None,
    }

def route_after_safety(state:AgentState)->AgentState:
    if state.get("is_safe", True) :
        return "execute"
    else :
        return "blocked"