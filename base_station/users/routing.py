
channel_routing = {
    "websocket.connect": "base_station.users.consumers.ws_add",
    "websocket.keepalive": "base_station.users.consumers.ws_add",
    "websocket.receive": "base_station.users.consumers.ws_message",
    "websocket.disconnect": "base_station.users.consumers.ws_disconnect",
}
