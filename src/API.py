from aiohttp import web
from src.IO import save_file, delete_file, get_file_path
import src.constants as const


async def upload(request):
    """
    Метод реализующий загрузку файлов

    :param request: запрос от клиента
    :return: ответ со статусом загрузки
    """
    hash_file = await save_file(request)
    data = {
        'status': const.STATUS_OK if hash_file else const.STATUS_FAILED,
        'hash': hash_file
    }
    return web.json_response(data)


async def delete(request):
    """
    Метод реализующий удаление файла

    :param request: запрос от клиента
    :return: ответ со статусом удаления
    """
    hash_file = request.match_info.get('hash_file', None)
    data = {'status': await delete_file(hash_file)}
    return web.json_response(data)


async def download(request):
    """
    Метод реализующий выгрузку файла

    :param request: запрос от клиента
    :return: файл или статус с ошибкой в случае необнаружения файла
    """
    hash_file = request.match_info.get('hash_file', None)
    file_path = await get_file_path(hash_file)
    if not file_path:
        data = {'status': const.STATUS_FILE_NOT_FOUND}
        return web.json_response(data)
    resp = web.FileResponse(file_path)
    return resp
