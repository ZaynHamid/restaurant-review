import websockets
import asyncio
import datetime
import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST_URL"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
)


connected_clients = set()

async def send_leaderboard():
    while True:
        if connected_clients:
            top_restaurant = r.zrevrange("restaurants", 0, 8, withscores=True)
            message = "Top Restaurants:\n" + "\n".join(
              f"{restaurant}: {score}"
                for i, (restaurant, score) in enumerate(top_restaurant)
            )
            message += f"\n\n⏰ Server Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await asyncio.gather(*(client.send(message) for client in connected_clients))

        await asyncio.sleep(5) 

async def handler(websocket):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"From client: {message}")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        await asyncio.gather(send_leaderboard())

asyncio.run(main())
