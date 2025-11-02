from datetime import datetime
from pathlib import Path
import asyncio

import aiofiles
import aiofiles.os
import aiohttp


BASE_DIR = Path(__file__).parent
CATS_DIR = BASE_DIR / 'cats'
URL = 'https://api.thecatapi.com/v1/images/search'

async def get_new_image_url():
    # Создать асинхронную сессию для выполнения HTTP-запроса.
    async with aiohttp.ClientSession() as session:
        # Выполнить асинхронный GET-запрос на указанный URL.
        response = await session.get(URL)
        data = await response.json()
        random_cat = data[0]['url']
        return random_cat


async def download_file(url):
    filename = url.split('/')[-1] 

    async with aiohttp.ClientSession() as session:
        result = await session.get(url)
        # Открыть файл для записи в двоичном режиме.
        async with aiofiles.open(CATS_DIR / filename, 'wb') as f:  
            # Прочитать содержимое ответа и записать его в файл.
            await f.write(await result.read())


async def download_new_cat_image():
    url = await get_new_image_url()
    await download_file(url)


async def create_dir(dir_name):
    await aiofiles.os.makedirs(
        dir_name,  
        exist_ok=True 
    )


async def list_dir(dir_name):
    # Асинхронно получить список файлов и поддиректорий в указанной директории.
    files_and_dirs = await aiofiles.os.listdir(dir_name)
    print("Скачанные файлы:")
    print(*files_and_dirs, sep='\n')    


async def main():
    await create_dir('cats') 
    tasks = [
        asyncio.ensure_future(download_new_cat_image()) for _ in range(3)
    ]

    await asyncio.wait(tasks)
    await list_dir('cats')


if __name__ == '__main__':
    start_time = datetime.now()
    
    asyncio.run(main())

    end_time = datetime.now()

    print(f'Время выполнения программы: {end_time - start_time}.')
