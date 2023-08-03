from sessions.day1 import DAY1
from sessions.day2 import DAY2
from sessions.day3 import DAY3
from sessions.day4 import DAY4


from cc_blocks import SessionBlocks, save
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(r"/Volumes/Pdata/OFL/ofl-repeated dataset")


@dataclass
class Session:
    session_name: str
    sub_dir: str
    session_blocks: SessionBlocks


SESSIONS = [
    Session("day1", "01-day1", DAY1),
    Session("day2", "02-day2", DAY2),
    Session("day3", "03-day3", DAY3),
    Session("day4", "04-day4", DAY4),
]


def main():
    for session in SESSIONS:
        session_dir = ROOT_DIR / session.sub_dir
        session_dir.mkdir(exist_ok=True)
        fn = session_dir / "session_blocks.pkl"
        print(f"Saving session {session.session_name} to {str(fn)}")

        save(session, fn)


if __name__ == "__main__":
    main()
