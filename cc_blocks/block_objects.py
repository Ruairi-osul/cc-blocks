from dataclasses import dataclass
from typing import Optional
from typing import List, Dict


@dataclass(slots=True, frozen=True)
class BlockType:
    """A class representing a type of block in a session."""

    name: str
    duration: float
    block_group: Optional[str] = None
    description: str = ""


@dataclass(slots=True, frozen=True)
class BlockEvent:
    """A class representing an instance of a block in a session."""

    block_type: BlockType
    start_time: float


@dataclass(slots=True)
class SessionBlocks:
    """A class representing a session composed of blocks."""

    session_name: str
    block_types: Dict[str, BlockType]
    block_events: List[BlockEvent]

    def get_block_starts(self, block_name: str) -> List[float]:
        """Get the start times of a specific block within the session."""
        try:
            assert block_name in self.block_types.keys()
        except AssertionError:
            raise ValueError(
                f"Unknown block name '{block_name}'. Try one of {list(self.block_types.keys())}"
            )

        start_times = []
        for event in self.block_events:
            if event.block_type.name == block_name:
                start_times.append(event.start_time)

        return start_times

    def get_unique_block_types(self) -> List[str]:
        """Get a list of unique block types in the session."""
        return list(self.block_types.keys())
