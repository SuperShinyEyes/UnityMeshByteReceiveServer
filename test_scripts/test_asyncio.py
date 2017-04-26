import asyncio

def decrement(n):
    return n - 1

# Borrowed from http://curio.readthedocs.org/en/latest/tutorial.html.
# @asyncio.coroutine
# def countdown(number, n, t=1):
#     while n > 0:
#         print('T-minus', n, '({})'.format(number))
#         yield from asyncio.sleep(t)
#         # n -= 1
#         n = decrement(n)

async def countdown(number, n, t=1):
    while n > 0:
        print('T-minus', n, '({})'.format(number))
        await asyncio.sleep(t)
        # n -= 1
        n = decrement(n)

loop = asyncio.get_event_loop()  
tasks = [  
    asyncio.ensure_future(countdown("A", 2, t=3)),
    asyncio.ensure_future(countdown("B", 3))]
loop.run_until_complete(asyncio.wait(tasks))  
loop.close()
