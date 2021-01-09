from io import BytesIO
import os
import hashlib
import src.constants as const


async def save_file(multipart):
    async for obj in multipart:
        if obj.filename is not None:
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
    file_path = os.path.join(const.DIRECTORY_STORE_NAME, hash_file[0:2])
    file_path = os.path.join(file_path, hash_file)
    if not os.path.isfile(file_path):
        return const.STATUS_FILE_NOT_FOUND
    os.remove(file_path)
    return const.STATUS_OK


async def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)


async def get_hash(data):
    return hashlib.md5(data).hexdigest()
