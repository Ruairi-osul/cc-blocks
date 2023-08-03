from cc_blocks import BlockType, SessionBlocks, create_block_events
from typing import List

block_types = {
    "baseline": BlockType(
        name="baseline",
        duration=180,
        description="Baseline recording at the start of the session",
    ),
    "CS": BlockType(
        name="CS",
        duration=30,
        description="Conditioned stimulus presentation",
    ),
    "ITI": BlockType(
        name="ITI",
        duration=30,
        description="Inter-trial interval",
    ),
}

block_sequence: List[BlockType] = [block_types["baseline"]] + (
    30 * [block_types["CS"], block_types["ITI"]]
)
block_event_sequence = create_block_events(block_sequence)

RET = SessionBlocks(
    session_name="RET",
    block_types=block_types,
    block_events=block_event_sequence,
)
