import asyncio

from app.db.session import async_session
from app.repository.category_repository import CategoryRepo


async def fetch_parents():
    async with async_session() as session:
        repo = CategoryRepo(session)
        parents = await repo.get_parent_categories()
        for parent in parents:
            print(parent.id, parent.name)

asyncio.run(fetch_parents())