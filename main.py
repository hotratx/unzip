import re
import shutil
import rarfile
from typing import List
from zipfile import ZipFile
from pathlib import Path


class Unzip:
    pattern = re.compile(r"\d{4}_\d{2}_\d{2}.*(\.rar|\.zip)")
    quant_unzip = 0

    def __init__(self, paths: List) -> None:
        self.paths = paths

    def _search_files_zip(self, path: Path) -> List[Path]:
        """Filtra os arquivos da pasta path, retornarndo apenas arquivos .zip e que
            possuem o padrão do regex pattern.

        Args:
            path: Path da pasta com arquivos para ser analisado.

        Return:
            List: lista com os path dos arquivos que correspondem ao procurado
        """
        return [
            p for p in path.iterdir() if self.pattern.search(p.name)
        ]

    def _search_folders_empresas(self, path: Path) -> List[Path]:
        """Filtra as pasta contidas do path

        Args:
            path: Path da pasta que contem as pastas das empresas.

        Return:
            List: lista com os path das pastas das empresas.
        """
        return [p for p in path.iterdir() if p.is_dir()]

    def _handle_names(self, path: Path) -> List[Path]:
        """Manipula o path do arquivo.zip para retornar os paths das
            pastas de backup e de armazenamento dos aquivos extraidos e
            o path sem suffix.

        Args:
            path: Path do aquivo .zip

        Return:
            path_no_suffix: Path sem suffix
            folder: Path da pasta que representa o mês
            folder2: Path da pasta onde serão armazenados os arquivos extraidos
            backup: Path da pasta de backup que armazena os arquivos originais .zip
        """
        path_no_suffix = path.with_suffix("")
        _list_names = path_no_suffix.name.split("_")[:2]
        _name_folder = f"{_list_names[0]}_{_list_names[1]}"
        folder = path.parent / _name_folder
        folder2 = path.parent / _name_folder / path_no_suffix.name
        backup = path.parent / "backup"
        return [folder, folder2, backup ]

    def _create_folders(self, folder: Path, folder2: Path, backup: Path):
        """Cria as novas pastas

        Args:
            folder: path da pasta referente ao mês
            folder: path da pasta que irá receber dados extraidos
            backup: path da pasta de backup

        Return: 
            None
        """
        if not folder.exists():
            folder.mkdir()

        elif not folder.is_dir():
            folder.mkdir()

        if not folder2.exists():
            folder2.mkdir()

        if not backup.exists():
            backup.mkdir()

    def _extract_zip(self, path: Path) -> None:
        """Orquestra as funções de manipulação do Path, criação
        das novas pastas e unzip dos arquivos.

        Args:
            path: Path do arquivo original .zip

        Return:
            None
        """
        folder, folder2, backup = self._handle_names(path)

        self._create_folders(folder, folder2, backup)

        self._unzip(path, folder2, backup)

    def _unzip(self, file_name: Path, folder: Path, backup: Path) -> None:
        """Extrai os arquivos zipados para a nova pasta, e move o
        arquivo original .zip para a pasta de backup

        Args:
            file_name: Path do arquivo original
            folder: Path da pasta referente ao mês

        Return:
            None
        """
        if file_name.suffix == '.zip':
            with ZipFile(str(file_name), "r") as zip:
                zip.extractall(str(folder))
        elif file_name.suffix == '.rar':
            with rarfile.RarFile(str(file_name)) as rar:
                rar.extractall(str(folder))
        try:
            shutil.move(file_name, backup)
        except:
            print(
                f"o arquivo {file_name} já está na pasta de backup, logo será deletado!"
            )
            file_name.unlink()

        self.quant_unzip += 1

    def _analise_folder(self, folders_empresas) -> None:
        """Percore a lista de Paths das empresas

        Args:
            folders_empresas: lista com os path das empresas

        Return:
            None
        """
        for p in folders_empresas:
            files = self._search_files_zip(p)
            if files:
                _ = list(map(self._extract_zip, files))

    def run(self) -> None:
        """Inicia o a busca rercursica pelos arquivos .zip
        """
        self.quant_unzip = 0
        for path in self.paths:
            p1 = Path(path)
            folders_empresas = self._search_folders_empresas(p1)
            self._analise_folder(folders_empresas)

        if self.quant_unzip:
            print(f"Foram extraidos dados de {self.quant_unzip} arquivos .zip")
        else:
            print("Não foram encontrados arquivos .zip para serem extraidos dados")


if __name__ == "__main__":
    from sys import platform

    if platform == "linux" or platform == "linux2":
        folder_path = ['/home/hotratx/ttttest']
    elif platform == 'win32':
        folder_path = [r'C:\Users\hotratx\Desktop\teste']
    elif platform == 'darwin':
        folder_path = ['/User/hotratx/ttttest']
    else:
        folder_path = []

    unzip = Unzip(folder_path)
    unzip.run()
