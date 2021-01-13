from io import BytesIO
import os
import hashlib
import src.constants as const


async def save_file(request):
    """
    Метод сохраняющий файл локально

    :param request: запрос от клиента
    :return: хеш-код файла
    """
    async for obj in await request.multipart():
        if obj.filename:
            data = await obj.read()
            file = BytesIO(data)
        else:
            return None
        await create_directory(const.DIRECTORY_STORE_NAME)
        hash_file = await get_hash(data)
        path = os.path.join(const.DIRECTORY_STORE_NAME, hash_file[0:2])
        await create_directory(path)
        with open(os.path.join(path, hash_file), 'wb') as f:
            f.write(file.getvalue())
        f.close()
        return hash_file


async def delete_file(hash_file):
    """
    Удаление файла по хеш коду

    :param hash_file: хаш-код файла
    :return: статус
    """
    file_path = await get_file_path(hash_file)
    if not file_path:
        return const.STATUS_FILE_NOT_FOUND
    os.remove(file_path)
    return const.STATUS_OK


async def get_file_path(hash_file):
    """
    Получение пути файла по хещ-коду

    :param hash_file: хеш код файла
    :return: путь файла
    """
    file_path = os.path.join(const.DIRECTORY_STORE_NAME, hash_file[0:2])
    file_path = os.path.join(file_path, hash_file)
    if not os.path.isfile(file_path):
        return None
    return file_path


async def create_directory(path):
    """
    Метод создания директории

    :param path: путь
    """
    if not os.path.exists(path):
        os.mkdir(path)


async def get_hash(data):
    """
    Метод получение хеш-кода файла
    :param data: содержимое файла
    :return: хеш-код
    """
    return hashlib.md5(data).hexdigest()
