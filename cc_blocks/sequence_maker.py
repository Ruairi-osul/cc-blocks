from typing import List
from .block_objects import BlockType, BlockEvent


def create_block_events(
    block_types: List[BlockType], start_time: float = 0.0
) -> List[BlockEvent]:
    """Create a sequence of BlockEvent instances from a list of BlockType instances.

    Parameters
    ----------
    block_types : List[BlockType]
        A list of BlockType instances.
    start_time : float, optional
        The start time of the first block. The subsequent blocks will start one after another based on their duration.

    Returns
    -------
    List[BlockEvent]
        A list of BlockEvent instances.
    """
    block_events = []
    for block_type in block_types:
        block_event = BlockEvent(block_type=block_type, start_time=start_time)
        block_events.append(block_event)
        start_time += block_type.duration
    return block_events
