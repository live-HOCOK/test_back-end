from aiohttp import web
from src.IO import save_file, delete_file, get_file_path
import src.constants as const


async def upload(request):
    hash_file = await save_file(request)
    data = {
        'status': const.STATUS_OK if hash_file else const.STATUS_FAILED,
        'hash': hash_file
    }
    return web.json_response(data)


async def delete(request):
    hash_file = request.match_info.get('hash_file', None)
    data = {'status': await delete_file(hash_file)}
    return web.json_response(data)


async def download(request):
    hash_file = request.match_info.get('hash_file', None)
    file_path = await get_file_path(hash_file)
    if not file_path:
        data = {'status': const.STATUS_FILE_NOT_FOUND}
        return web.json_response(data)
    resp = web.FileResponse(file_path)
    return resp
