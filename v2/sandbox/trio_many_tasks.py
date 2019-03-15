
import trio

async def main():
    async with trio.open_nursery() as nursery:
        for _ in range(100000):
            nursery.start_soon(trio.sleep, 30)

trio.run(main)
