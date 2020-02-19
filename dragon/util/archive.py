import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Literal

# from typing import Literal, List
# from functools import singledispatch

SUPPORTED_ARCHIVED_TYPE = Literal['zip']
__ARCHIVED_TYPE = Literal['zip', 'tar', 'gztar', 'bztar', 'xztar']

__archived_file_format_type_names = [typename for typename, _ in shutil.get_archive_formats()]

__supported_archived_suffix_dict = [(suffix, format_type)
                                    for format_type, suffixes, _ in shutil.get_unpack_formats()
                                    for suffix in suffixes]


def get_arctype(filename: str) -> str:
    for k, v in __supported_archived_suffix_dict:
        if filename.endswith(k):
            return v
    raise Exception('not support this archived file type')


def compress_folder(achieved_basename: str, format_type: Literal['zip'], src_folder: Path,
                    dest_folder: Path) -> Path:
    if not src_folder.is_dir():
        raise Exception('only can compress a folder path')
    dest_basename_path = dest_folder / f'{achieved_basename}'
    return Path(shutil.make_archive(str(dest_basename_path), format_type, src_folder))


def compress_single_or_more_files(achieved_basename: str, format_type: Literal['zip'], *src: Path,
                                  dest_folder: Path) -> Path:

    for file_or_dir in src:
        if file_or_dir.is_dir():
            raise Exception(f'{file_or_dir.name} is a dir not supported for this compress function')
    dest_basename_path = dest_folder / f'{achieved_basename}'
    with TemporaryDirectory() as temp_dir:
        for file_ in src:
            shutil.copy2(file_, temp_dir / Path(file_.name))
        return Path(shutil.make_archive(str(dest_basename_path), format_type, temp_dir))


def compress2(
        achieved_basename: str,
        format_type: Literal['zip'],
        *src: Path,
        dest_dir: Path = Path.cwd(),
        callback: Callable[[], None] = None,
) -> Path:

    dest_basename_path = dest_dir / f'{achieved_basename}'
    with TemporaryDirectory() as temp_dir:
        for file_or_dir in src:
            if file_or_dir.is_dir():
                shutil.copytree(file_or_dir,
                                temp_dir / Path(file_or_dir.name),
                                ignore_dangling_symlinks=True)
            else:
                shutil.copy2(file_or_dir, temp_dir / Path(file_or_dir.name))
            if callback:
                callback()
        return Path(shutil.make_archive(str(dest_basename_path), format_type, temp_dir))


def compress_processing(achieved_basename: str,
                        format_type: str,
                        *src: Path,
                        dest_dir: Path = Path.cwd(),
                        loading_cnt: int = 0):
    if format_type not in __archived_file_format_type_names:
        raise Exception(f"not support this archived file type: {format_type}")

    dest_basename_path = dest_dir / f'{achieved_basename}'
    yield loading_cnt
    with TemporaryDirectory() as temp_dir:
        for file_or_dir in src:
            if file_or_dir.is_dir():
                shutil.copytree(
                    file_or_dir,
                    temp_dir / Path(file_or_dir.name),
                    symlinks=True,
                )
            else:
                shutil.copy2(file_or_dir, temp_dir / Path(file_or_dir.name))
            loading_cnt += 10
            yield loading_cnt
        shutil.make_archive(str(dest_basename_path), format_type, temp_dir)


# @singledispatch
# def compress(achieved_basename, format_type, src, dest_dir):
#     pass


def compress(achieved_basename: str, format_type: Literal['zip'], src: Path,
             dest_folder: Path) -> Path:
    if not dest_folder.exists() or not dest_folder.is_dir():
        raise Exception('dest_dir must be a directory path')
    dest_basename_path = dest_folder / f'{achieved_basename}'
    if src.is_dir():
        # achieve files
        return Path(shutil.make_archive(str(dest_basename_path), format_type, src))
    else:
        # achieve single file
        with TemporaryDirectory() as temp_dir:
            shutil.copy2(src, temp_dir / Path(src.name))
            return Path(shutil.make_archive(str(dest_basename_path), format_type, temp_dir))


# @compress.register
# def more(achieved_basename: str, format_type: Literal['zip'],
#          src_folder: List[Path], dest_folder: Path):
#     if not dest_folder.exists() or not dest_folder.is_dir():
#         raise Exception('dest_dir must be a directory path')

#     for file_or_dir in src_folder:
#         if file_or_dir.is_dir():
#             raise Exception(
#                 f'{file_or_dir.name} is a dir not supported for this compress function'
#             )

#     dest_basename_path = dest_folder / f'{achieved_basename}'


def extract_all(achieved_path: Path, dest_dir: Path):
    if dest_dir.is_dir():
        shutil.unpack_archive(str(achieved_path), extract_dir=dest_dir)
    else:
        raise Exception('dest_dir must be a directory path')


if __name__ == "__main__":
    print('Debug Done')
