import pickle
from .block_objects import SessionBlocks

def save(obj: SessionBlocks, filename: str) -> None:
    """Save a SessionBlocks instance to disk.

    Parameters
    ----------
    obj : SessionBlocks
        The SessionBlocks instance to save.
    filename : str
        The name of the file to save the SessionBlocks instance to.
    """
    with open(filename, "wb") as f:
        pickle.dump(obj, f)
    return None

def load(filename: str) -> SessionBlocks:
    with open(filename, "rb") as f:
        obj = pickle.load(f)
    return obj