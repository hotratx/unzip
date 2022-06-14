from typing import List
from zipfile import ZipFile
from pathlib import Path


def all_files_zip(path: Path) -> List[Path]:
    """Lista todos os arquivos do path que são .zip"""
    return [p for p in path.iterdir() if p.suffix == '.zip']


def extract_zip(path: Path):
    file = path / str(path).split('.')[0]
    if file.exists() and file.is_dir():
        print(f'folder {file.name} já existe')
    else:
        print(f'criando folder para {file}')
        file.mkdir()
        unzip(file)


def unzip(file_name: Path):
    with ZipFile(str(file_name) + '.zip', "r") as zip:
        print("Extraindo todos os arquivos agora...")
        zip.extractall(str(file_name))
        print("Feito!")


def run(paths):
    for path in paths:
        p = Path(path)
        files = all_files_zip(p)
        if files:
            print(f'Todos arquivos zip encontrados: {files}')
            _ = list(map(extract_zip, files))


if __name__ == "__main__":
    folder_path = ['C:\\Users\\hotratx']
    x = run(folder_path)
