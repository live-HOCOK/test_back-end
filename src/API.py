from aiohttp import web
from src.IO import save_file, delete_file


async def upload(request):
    hash_file = await save_file(await request.multipart())
    data = {'hash': hash_file}
    return web.json_response(data)


async def delete(request):
    hash_file = request.match_info.get('hash_file', None)
    data = {'status': await delete_file(hash_file)}
    return web.json_response(data)


async def download(request):
    data = {'status': 'neOK'}
    return web.json_response(data)
