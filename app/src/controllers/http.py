# -*- coding: utf-8 -*-

import aiohttp
from aiohttp import ClientResponse
import asyncio

async def fetch(session, url, headers, cookies):
    async with session.get(url, headers=headers, cookies=cookies) as response:
        return await response.text()

async def main():
    url = "https://realt.by/account/my-objects/"  # URL вашего запроса

    # Заголовки запроса (при необходимости)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    # Куки запроса
    cookies = {
        "consent": "{\"analytics\":false,\"advertising\":false,\"functionality\":true}",
        "hasAuth": "1",
        "authToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NDAyNDg3MTUsImV4cCI6MTc3MTc4NDcxNSwidG9rZW5VdWlkIjoiNWM4MmY2MTYtZjE0YS0xMWVmLWFjZGEtMWVkNDM1YzA3NzhkIiwidXVpZCI6IjNkNDUyM2YwLWYxNGEtMTFlZi1iNTQwLTliZDI2ZmNjZDBjNiJ9.w1j3g3CkU0K7C5ryfOJlrUDwnBqbItSyZ6ww4xoGis01fZJ-yBUBaHJ9O024Jv99Sg6_Htft9RwiQsEHFSCljcqfNwH3GkAGA7mBZZK0OroG-pN4scEVQFcT2Kcl6uNy08NuF4L3UIWTcnddYfMicIH5l9Pvx_83VbbL3MbMKC12CYYVOjz0CGbriP7Rmh3DAbRD7FKdossH_arPDybO3RHTc7iy1QO1BX0YfI0FhV2Omp_nw4WjC0t0BlppJV6AexXfP9wIr9zfjNpvqgTQE5_b0UTDqx1V6hp80rebZa3J1tXfKF7tqo_qWMPJsmFfJ9_k_pg64NA3rhusAxDjQO98slcJW9F1IQhIhn_zmFHze8aOfzFaCph-SV2cFcKb-98VxTbQgx_748099Mv1X4wH2C0KmWjSJjXDmGcFR3tSv3sO6NR4NdEcG0kwEfXgYizUKsnCXcgJPn2HObmJj5FqXqNRWCxB4czU4t8WbBsMEYQCbNb4HnVcWI8LjBSfEXXS0Sy3IXC5LigrI2ekg2rUx5_vm7PGCiJEFppfYx8JH1vM1IuardmMySBPNIQXZmrzrxWhA6CUMnAf9WUu0FNHK2fjfzbjtMv3f31hLH3bLUDzXaBDi-eayS7JwrHjWNAhpUwyHdtBogC5g-7UBJ4k0sHO-N_CCep6ZuH2gjs",
        "realt_user": "132ebfc667d0623523b787e70a1592fe"
    }

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, headers, cookies) for _ in range(5)]  # 5 одновременных запросов
        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses, 1):
                with open(f'D:\\result{i}.html', 'wb') as f:
                    f.write(response.encode())

if __name__ == '__main__':
    asyncio.run(main())