import re
import shutil
import rarfile
from typing import List, Generator
from zipfile import ZipFile
from pathlib import Path


class Unzip:
    pattern = re.compile(r"\d{4}_\d{2}_\d{2}.*(\.rar|\.zip)")
    quant_unzip = 0

    def __init__(self, paths: List) -> None:
        self.paths = paths

    def _search_files_zip(self, path: Path) -> Generator:
        """Filtra os arquivos da pasta path, retornarndo apenas arquivos .zip 
            e que possuem o padrão do pattern regex.

        Args:
            path: Path da pasta com arquivos para ser analisado.

        Return:
            Generator: um gerador com os path dos arquivos que correspondem 
            ao procurado
        """
        anos = [p for p in path.iterdir() if p.is_dir()]
        for ano in anos:
            meses = [p for p in ano.iterdir() if p.is_dir()]
            for mes in meses:
                files_zip = [p for p in mes.iterdir() if self.pattern.search(p.name)]
                for file in files_zip:
                    yield file

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
            pastas de backup e de armazenamento dos aquivos extraídos.
        Args:
            path: Path do aquivo .zip

        Return:
            folder: Path da pasta onde serão armazenados os arquivos extraídos
            backup: Path da pasta de backup que armazena os arquivos originais .zip
        """
        path_no_suffix = path.with_suffix("")
        folder = path.parent / path_no_suffix.name
        backup = path.parent / "backup"
        return [folder, backup]

    def _create_folders(self, folder: Path, backup: Path):
        """Cria as novas pastas

        Args:
            folder: path da pasta referente ao mês
            folder: path da pasta que irá receber dados extraídos
            backup: path da pasta de backup

        Return:
            None
        """
        if not folder.exists():
            folder.mkdir()

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
        folder, backup = self._handle_names(path)

        self._create_folders(folder, backup)

        self._unzip(path, folder, backup)

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
        for emp in folders_empresas:
            files_zip = self._search_files_zip(emp)
            if files_zip:
                _ = list(map(self._extract_zip, files_zip))

    def run(self) -> None:
        """Inicia o a busca recursiva pelos arquivos .zip
        """
        self.quant_unzip = 0
        for path in self.paths:
            p1 = Path(path)
            folders_empresas = self._search_folders_empresas(p1)
            self._analise_folder(folders_empresas)

        if self.quant_unzip:
            print(f"Foram extraídos dados de {self.quant_unzip} novos arquivos.zip")
        else:
            print("Não foram encontrados novos arquivos.zip!")


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
