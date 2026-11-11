import shutil
from pathlib import Path

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Programs": [".py", ".java", ".cpp", ".c", ".js", ".ts", ".html", ".css", ".php", ".cs"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Others": []
}


def get_category(file_name: str) -> str:
    extension = Path(file_name).suffix.lower()

    for category, extensions in file_types.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_destination(folder: Path, file_name: str) -> Path:
    destination = folder / file_name

    if not destination.exists():
        return destination

    name = Path(file_name)
    stem = name.stem
    suffix = name.suffix
    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        candidate = folder / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(folder_path: str) -> bool:
    folder = Path(folder_path).expanduser().resolve()

    if not folder.is_dir():
        return False

    current_file = Path(__file__).resolve()

    for item in folder.iterdir():
        if not item.is_file():
            continue

        if item.resolve() == current_file:
            continue

        category = get_category(item.name)
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = get_unique_destination(destination_folder, item.name)
        shutil.move(str(item), str(destination))
        print(f"{item.name} moved to {category}")

    print("\nFile organization completed!")
    return True


if __name__ == "__main__":
    user_input = input("Enter folder path: ").strip()

    if not user_input:
        print("Folder path cannot be empty!")
    elif not organize_folder(user_input):
        print("Invalid folder path!")