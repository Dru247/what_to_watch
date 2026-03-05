"""Работа с API Dropbox."""
import asyncio
import json
from typing import List

import aiohttp

from opinions_app import app


AUTH_HEADER = f'Bearer {app.config['DROPBOX_TOKEN']}'
UPLOAD_LINK = 'https://content.dropboxapi.com/2/files/upload'
SHARING_LINK = (
    'https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings'
)


# def upload_files_to_dropbox(images) -> list:
#     """Загружает фалы в Dropbox."""
#     urls = []
#     if images is not None:
#         start_time = time.time()
#         for image in images:
#             dropbox_args = json.dumps({
#                 'autorename': True,
#                 'path': f'/{image.filename}'
#             })
#             print(f'Загрузка изображения {image.filename}')
#             response = requests.post(
#                 UPLOAD_LINK,
#                 headers={
#                     'Authorization': AUTH_HEADER,
#                     'Dropbox-API-Arg': dropbox_args,
#                     'Content-Type': 'application/octet-stream'
#                 },
#                 data=image.read()
#             )
#             path = response.json()['path_lower']
#             print(f'Получение ссылки для {image.filename}')
#             response = requests.post(
#                 SHARING_LINK,
#                 headers={'Authorization': AUTH_HEADER},
#                 json={'path': path}
#             )
#             data = response.json()
#             if 'url' not in data:
#                 # Обходной манёвр на случай, 
#                 # если пользователь попытается отправить
#                 # один и тот же файл дважды. Ему вернётся
#                 # ссылка на уже существующий файл.
#                 data = data['error']['shared_link_already_exists']['metadata']
#             url = data['url']
#             # Заменить режим работы ссылки,
#             # чтобы получить ссылку на скачивание.
#             url = url.replace('&dl=0', '&raw=1')
#             urls.append(url)
#         final_time = time.time() - start_time
#         print(f'Итоговое время загрузки {final_time}')

#     return urls


async def upload_file_and_get_url(
    session: aiohttp.ClientSession,
    image
) -> str:
    """Асинхронная функция загрузки изображения и получения на них ссылки."""
    dropbox_args = json.dumps({
        'autorename': True,
        'mode': 'add',
        'path': f'/{image.filename}'
    })
    # Асинхронная загрузка в aiohttp выполняется
    # с помощью асинхронного контекстного менеджера.
    async with session.post(
        UPLOAD_LINK,
        headers={
            'Authorization': AUTH_HEADER,
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': dropbox_args
        },
        data=image.read()
    ) as response:
        # Асинхронное получение ответа должно сопровождаться
        # ключевым словом await.
        data = await response.json()
        path = data['path_lower']

    async with session.post(
        SHARING_LINK,
        headers={
            'Authorization': AUTH_HEADER,
            'Content-Type': 'application/json'
        },
        json={'path': path}
    ) as response:
        data = await response.json()
        if 'url' not in data:
            data = data['error']['shared_link_already_exists']['metadata']
        url = data['url']
        url = url.replace('&dl=0', '&raw=1')

    return url


async def async_upload_files_to_dropbox(images) -> List[str]:
    """Создаёт задачи загрузки фото и запускает их асинхронно."""
    if images is not None:
        # Список асинхронных задач.
        tasks = []
        # Инициализация единой сессии.
        async with aiohttp.ClientSession() as session:
            for image in images:
                # Для каждого изображения создаём асинхронную задачу.
                tasks.append(
                    asyncio.ensure_future(
                        # передаём в асинхронную функцию сессию и изображение.
                        upload_file_and_get_url(session, image)
                    )
                )
            # После создания всех функций, запускаем их.
            urls = await asyncio.gather(*tasks)
        return urls
