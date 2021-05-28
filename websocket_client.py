import asyncio
# 웹 소켓 모듈을 선언한다.
import websockets

async def connect():
    # 웹 소켓에 접속을 합니다.
    async with websockets.connect("ws://192.168.0.182:9998") as websocket:
        # 웹소켓 서버에 메시지를 전송
        await websocket.send("hello websocket!!");
        # 웹 소켓 서버로 부터 메시지가 오면 콘솔에 출력합니다.
        data = await websocket.recv();
        print(data);


# 비동기로 서버에 접속한다.
asyncio.get_event_loop().run_until_complete(connect())