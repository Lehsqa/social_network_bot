import asyncio
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
import random
import json


with open('config.json') as config_file:
    config = json.load(config_file)

base_url = 'http://localhost:4000/api'
posts_id = []


async def action(s, users):
    try:
        async with s.post(f'{base_url}/signup', json={'username': f'bot{users}', 'password': 'pass'}) as r:
            if r.status != 200:
                print(await r.json())

        async with s.post(f'{base_url}/login', json={'username': f'bot{users}', 'password': 'pass'}) as r:
            if r.status != 200:
                r.raise_for_status()
            token = await r.json()

        for _ in range(config['max_posts_per_user']):
            async with s.post(f'{base_url}/posts', json={'content': f'Some text {users}'},
                              headers={'Authorization': f'Bearer {token["access_token"]}'}) as r:
                if r.status != 200:
                    r.raise_for_status()
                post = await r.json()
                posts_id.append(post['id'])
                print(post)

        for _ in range(config['max_likes_per_user']):
            async with s.post(f'{base_url}/posts/{random.choice(posts_id)}/like', json={},
                              headers={'Authorization': f'Bearer {token["access_token"]}'}) as r:
                print(await r.json())

        return {f'Bot {users}': 'finish'}
    except ClientConnectorError:
        return {f'Bot {users}': 'error connection'}


async def action_all(s, users):
    tasks = []
    for user in users:
        task = asyncio.create_task(action(s, user))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def main():
    users = range(1, config['number_of_users'] + 1)
    async with aiohttp.ClientSession() as session:
        print(await action_all(session, users))


if __name__ == '__main__':
    if not(isinstance(config['number_of_users'], int)) or not(isinstance(config['max_posts_per_user'], int)) or \
            not(isinstance(config['max_likes_per_user'], int)):
        print("Please, check data type from config file for validity (must be int type)")
        exit(1)
    asyncio.run(main())
