import os
import shutil


def _copy_directory_contents(source_dir, destination_dir):
    for entry in os.listdir(source_dir):
        source_path = os.path.join(source_dir, entry)
        destination_path = os.path.join(destination_dir, entry)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} -> {destination_path}")
        else:
            os.mkdir(destination_path)
            _copy_directory_contents(source_path, destination_path)


def copy_directory_recursive(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    os.mkdir(destination_dir)
    _copy_directory_contents(source_dir, destination_dir)


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(project_root, "static")
    destination_dir = os.path.join(project_root, "public")
    copy_directory_recursive(source_dir, destination_dir)


if __name__ == "__main__":
    main()

