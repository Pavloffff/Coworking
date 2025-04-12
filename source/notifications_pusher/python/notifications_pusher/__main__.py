import asyncio

from notifications_pusher.notifications_pusher import NotificationsPusher


if __name__ == "__main__":
    app = NotificationsPusher()
    asyncio.run(app.run())
