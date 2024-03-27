from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set
import pandas as pd
from .block_objects import BlockType, BlockEvent


@dataclass(slots=True)
class SessionBlocks:
    """A class representing a session composed of blocks."""

    session_name: str
    block_sequence: List[BlockEvent]

    @property
    def block_types(self) -> Set[BlockType]:
        """Get the set of block types in the session."""
        return {event.block_type for event in self.block_sequence}

    @property
    def block_groups(self) -> Set[str]:
        """Get the set of block groups in the session."""
        return {block_type.block_group for block_type in self.block_types}

    def get_block_starts(
        self, block_name: Optional[str] = None, block_group: Optional[str] = None
    ) -> List[float]:
        """Get the start times of a specific block within the session."""
        if block_name is not None:
            return self._get_block_starts_by_block_name(block_name)
        elif block_group is not None:
            return self._get_block_starts_by_block_group(block_group)
        else:
            raise ValueError("Either block_name or block_group must be specified.")

    def _get_block_starts_by_block_name(self, block_name: str) -> List[float]:
        """Get the start times of a specific block within the session."""
        if block_name not in {block_type.name for block_type in self.block_types}:
            raise ValueError(f"Unknown block name '{block_name}'")

        start_times = []
        for event in self.block_sequence:
            if event.block_type.name == block_name:
                start_times.append(event.start_time)

        return start_times

    def _get_block_starts_by_block_group(self, block_group: str) -> List[float]:
        """Get the start times of a specific block within the session."""
        if block_group not in self.block_groups:
            raise ValueError(f"Unknown block group '{block_group}'")

        start_times = []
        for event in self.block_sequence:
            if event.block_type.block_group == block_group:
                start_times.append(event.start_time)

        return start_times

    def get_block_time_series(self, sampling_rate: float) -> pd.DataFrame:
        """Get a time series of block types. Return as a pandas DataFrame with columns ["time", "block_type", "block_group"]."""

        time = []
        block_type = []
        block_group = []  # Assuming block_group is an attribute of block_type

        cumulative_time = 0
        for event in self.block_sequence:
            duration = int(event.block_type.duration * sampling_rate)
            block_type += [event.block_type.name] * duration
            block_group += [
                event.block_type.block_group
            ] * duration  # Assuming block_group is an attribute of block_type
            time += list(range(cumulative_time, cumulative_time + duration))
            cumulative_time += duration

        return pd.DataFrame(
            {"time": time, "block_type": block_type, "block_group": block_group}
        )

    def get_binary_block_time_series(
        self,
        sampling_rate: float,
        block_name: Optional[str] = None,
        block_group: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get a time series of binary block types indicating whether a block is present or not. Return as a pandas DataFrame with columns ["time", "in_block"]."""
        if block_name is not None:
            return self._get_binary_block_time_series_by_bkock_name(
                sampling_rate, block_name
            )
        elif block_group is not None:
            return self._get_binary_block_time_series_by_block_group(
                sampling_rate, block_group
            )
        else:
            raise ValueError("Either block_name or block_group must be specified.")

    def _get_binary_block_time_series_by_bkock_name(
        self, sampling_rate: float, block_name: str
    ) -> pd.DataFrame:
        """Get a time series of binary block types indicating whether a block is present or not. Return as a pandas DataFrame with columns ["time", "in_block"]."""

        if block_name not in {block_type.name for block_type in self.block_types}:
            raise ValueError(f"Unknown block name '{block_name}'")
        df = self.get_block_time_series(sampling_rate)
        df["in_block"] = df["block_type"] == block_name
        df = df.loc[:, ["time", "in_block"]]
        return df

    def _get_binary_block_time_series_by_block_group(
        self, sampling_rate: float, block_group: str
    ) -> pd.DataFrame:
        """Get a time series of binary block types indicating whether a block is present or not. Return as a pandas DataFrame with columns ["time", "in_block"]."""

        if block_group not in self.block_groups:
            raise ValueError(f"Unknown block group '{block_group}'")
        df = self.get_block_time_series(sampling_rate)
        df["in_block"] = df["block_group"] == block_group
        df = df.loc[:, ["time", "in_block"]]
        return df


@dataclass(slots=True)
class GroupedSessionBlocks:
    """"""

    session_name: str
    grouped_sessionblocks: Dict[str, SessionBlocks]

    @property
    def block_types(self) -> Set[BlockType]:
        """Get the set of block types across all grouped session blocks."""
        return {
            event.block_type
            for sb in self.grouped_sessionblocks.values()
            for event in sb.block_sequence
        }

    @property
    def block_groups(self) -> Set[str]:
        """Get the set of block groups across all grouped session blocks."""
        return {block_type.block_group for block_type in self.block_types}

    def get_block_starts(
        self, block_name: Optional[str] = None, block_group: Optional[str] = None
    ) -> pd.DataFrame:
        """Get the start times of a specific block in each grouped session.

        Return as a pandas DataFrame with columns ["group_name", "block_name", "block_group", "start_time",].
        """

        df_list = []
        for group_name, group_sb in self.grouped_sessionblocks.items():
            group_block_starts = group_sb.get_block_starts(
                block_name=block_name, block_group=block_group
            )
            df_group_block_starts = pd.DataFrame(
                group_block_starts, columns=["start_time"]
            )
            df_group_block_starts["group_name"] = group_name
            df_group_block_starts["block_name"] = block_name
            df_group_block_starts["block_group"] = block_group
            df_list.append(df_group_block_starts)

        df_block_starts = pd.concat(df_list, ignore_index=True)
        df_block_starts = df_block_starts[
            ["group_name", "block_name", "block_group", "start_time"]
        ]
        return df_block_starts

    def get_block_time_series(self, sampling_rate: float) -> pd.DataFrame:
        """Get a time series of block types for each grouped session.

        Return as a pandas DataFrame with columns ["time", "group_name",  "block_type", "block_group"].
        """

        df_list = []
        for group_name, group_sb in self.grouped_sessionblocks.items():
            df_group_block_time_series = group_sb.get_block_time_series(sampling_rate)
            df_group_block_time_series["group_name"] = group_name
            df_list.append(df_group_block_time_series)

        df_block_time_series = pd.concat(df_list, ignore_index=True)
        df_block_time_series = df_block_time_series[
            ["time", "group_name", "block_type", "block_group"]
        ]
        return df_block_time_series

    def get_binary_block_time_series(
        self,
        sampling_rate: float,
        block_name: Optional[str] = None,
        block_group: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get a binary time series of block types for each grouped session.

        Return as a pandas DataFrame with columns ["time", "group_name", "in_block"].
        """
        df_list = []
        for group_name, group_sb in self.grouped_sessionblocks.items():
            df_group_binary_block_time_series = group_sb.get_binary_block_time_series(
                sampling_rate, block_name=block_name, block_group=block_group
            )
            df_group_binary_block_time_series["group_name"] = group_name
            df_list.append(df_group_binary_block_time_series)

        df_binary_block_time_series = pd.concat(df_list, ignore_index=True)
        df_binary_block_time_series = df_binary_block_time_series[
            ["time", "group_name", "in_block"]
        ]
        return df_binary_block_time_series
