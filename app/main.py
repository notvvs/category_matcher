import asyncio

from app.db.session import async_session
from app.repository.postgres_repository import CategoryRepo


async def fetch_parents():
    async with async_session() as session:
        repo = CategoryRepo(session)
        parents = await repo.get_parent_categories()
        for parent in parents:
            print(parent.name)
            child = await repo.get_children('Скейтбординг')
            print(child)

asyncio.run(fetch_parents())