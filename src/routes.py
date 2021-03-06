from aiohttp import web
from src.API import upload, delete, download


def setup_routes(app):
    """
    Метод добавления маршрутов

    :param app: экземпляр приложения
    """
    app.add_routes([
        web.post('/upload', upload),
        web.get('/delete/{hash_file}', delete),
        web.get('/download/{hash_file}', download)
    ])
