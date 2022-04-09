"""
Websocket Application
"""


async def websocket_application(scope, receive, send):
    """
    Default Websocket Application
    :param scope:
    :param receive:
    :param send:
    :return:
    """
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong!"})
