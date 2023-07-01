import asyncio
import interfaces.n1mm as n1mm
import interfaces.clublog as clublog

async def broadcast(qso_queue, services):
    try:
        while True:
            qso = await qso_queue.get()
            clublog.send_qso(qso)
            qso_queue.task_done();
    except asyncio.CancelledError:
        print('broadcast(): got canceled')
        raise
    finally:
        print('broadcast(): exiting')


async def main():
    print("Starting")

    qso_queue = asyncio.Queue()

    n1mm.start(qso_queue)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(broadcast(queue))

    print("Finished")

asyncio.run(main())
