"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

ALLOWED = {'idle': {'researching'}, 'researching': {'writing', 'failed'}, 'writing': {'reviewing', 'failed'}, 'reviewing': {'complete', 'failed'}, 'complete': set(), 'failed': set()}


def transition(state, target):
    if target not in ALLOWED.get(state, set()):
        raise ValueError(f'Illegal state transition: {state} -> {target}')
    return target


async def run(agent, data):
    state, history = 'idle', ['idle']
    result = None
    for target in ('researching', 'writing', 'reviewing'):
        state = transition(state, target)
        history.append(state)
        result = await agent.ask(state, 'Complete this state using the previous evidence.', {'goal': data['goal'], 'evidence': data['evidence'], 'previous': result}, data['evidence'])
    state = transition(state, 'complete')
    history.append(state)
    return {'state': state, 'history': history, 'result': result}
