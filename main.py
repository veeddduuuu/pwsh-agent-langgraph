from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

from agent.graph import build_graph, thread_config
from agent.state import AgentState

load_dotenv()


def _print_output(state: AgentState) -> None:
    if state.get("executed"):
        print(f"  exit    : {state.get('exit_code')}")
        stdout = state.get("stdout", "")
        stderr = state.get("stderr", "")
        if stdout:
            print("\n--- output ---")
            print(stdout.rstrip("\n"))
        if stderr:
            print("\n--- errors ---")
            print(stderr.rstrip("\n"))
    print()


def _run_once(graph, prompt: str, auto: bool) -> None:
    """Generate + screen (graph pauses), optionally confirm, then execute."""
    config = thread_config()

    # First leg: generate + safety. The graph interrupts before execute.
    graph.invoke({"prompt": prompt}, config)
    state: AgentState = graph.get_state(config).values

    command = state.get("command", "")
    if not command:
        print("Could not generate a command for that request.\n")
        return

    print(f"\n  command : {command}")
    if state.get("explanation"):
        print(f"  details : {state['explanation']}")

    if not state.get("is_safe", True):
        print(f"  [BLOCKED] {state.get('safety_reason', '')}")

    if not auto:
        answer = input("\nRun this command? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Skipped.\n")
            return

    # Second leg: resume to execute (or fall through to the blocked node).
    graph.invoke(None, config)
    final: AgentState = graph.get_state(config).values
    _print_output(final)


def _interactive(graph, auto: bool) -> None:
    print("WinCliAgent — type a request, or 'exit' to quit.")
    while True:
        try:
            prompt = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if prompt.lower() in {"exit", "quit", "q"}:
            break
        if not prompt:
            continue
        _run_once(graph, prompt, auto)


def main() -> int:
    parser = argparse.ArgumentParser(description="Natural language to Windows CLI agent.")
    parser.add_argument("prompt", nargs="*", help="The request to translate and run.")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Execute the generated command without asking for confirmation.",
    )
    args = parser.parse_args()

    graph = build_graph()

    if args.prompt:
        _run_once(graph, " ".join(args.prompt), args.auto)
    else:
        _interactive(graph, args.auto)
    return 0


if __name__ == "__main__":
    sys.exit(main())