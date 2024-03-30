import asyncio
from aiogram import Bot
import msg_text


class NotificationService:
    def __init__(self):
        self.task = None

    async def api_get_notifications(self):
        return [
            {'id': 339095791, 'type': 'start',
                'time': '09:00', 'room': 'room_1'},
            {'id': 339095791, 'type': 'end', 'time': '10:00', 'room': 'room_2'},]

    async def notifications_sender(self, bot: Bot):
        while True:
            notifications = await self.api_get_notifications()
            for notification in notifications:
                notification_template = msg_text.msg_notification_text_start if notification[
                    'type'] == 'start' else msg_text.msg_notification_text_end
                notification_text = notification_template.format(
                    time=notification['time'], room=notification['room'])
                await bot.send_message(chat_id=notification['id'], text=notification_text)
            await asyncio.sleep(15)

    async def start(self, bot: Bot):
        self.task = asyncio.create_task(self.notifications_sender(bot))

    async def stop(self):
        if self.task:
            self.task.cancel()
