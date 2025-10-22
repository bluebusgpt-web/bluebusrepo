from pathlib import Path
import shutil

DOWNLOADS = Path(r"C:\Users\student\Downloads")

TARGET_MAP = {
    ("jpg", "jpeg"): DOWNLOADS / "images",
    ("csv", "xlsx"): DOWNLOADS / "data",
    ("txt", "doc", "pdf"): DOWNLOADS / "docs",
    ("zip",): DOWNLOADS / "archive",
}

def ensure_dirs():
    for dest in {d for exts, d in TARGET_MAP.items()}:
        dest.mkdir(parents=True, exist_ok=True)

def unique_dest(path: Path, dest_dir: Path) -> Path:
    candidate = dest_dir / path.name
    if not candidate.exists():
        return candidate
    stem = path.stem
    suffix = path.suffix
    i = 1
    while True:
        candidate = dest_dir / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1

def move_file(src: Path, dest_dir: Path):
    dest = unique_dest(src, dest_dir)
    try:
        shutil.move(str(src), str(dest))
        print(f"Moved: {src.name} -> {dest_dir.name}\\{dest.name}")
    except Exception as e:
        print(f"Error moving {src}: {e}")

def organize_downloads():
    if not DOWNLOADS.exists():
        print(f"Downloads 폴더가 존재하지 않습니다: {DOWNLOADS}")
        return

    ensure_dirs()

    # 파일을 확장자별로 검색하여 이동
    for ext_group, dest_dir in TARGET_MAP.items():
        for ext in ext_group:
            for path in DOWNLOADS.glob(f"*.{ext}"):
                if path.is_file():
                    move_file(path, dest_dir)
            # 대소문자 확장자 처리 (예: .JPG)
            for path in DOWNLOADS.glob(f"*.{ext.upper()}"):
                if path.is_file():
                    move_file(path, dest_dir)

if __name__ == "__main__":
    organize_downloads()