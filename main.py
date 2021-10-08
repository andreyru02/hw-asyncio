import sqlite3
import asyncio
from email.message import EmailMessage
import aiosmtplib
import ssl


def get_users():
    with sqlite3.connect('contacts.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM contacts")
        user = cursor.fetchall()
        users = set(user)
        users_list = []
        for user in users:
            users_list.append(user)
        return users_list


async def create_message(contact_id, first_name, last_name, email, address):
    message = EmailMessage()
    message["From"] = 'root@localhost'
    message["To"] = email
    message["Subject"] = "Спасибо!"
    message.set_content(f"Уважаемый {first_name} {last_name} !\n"
                        "Спасибо, что пользуетесь нашим сервисом объявлений.")
    return message


async def send_message(message):
    context = ssl.create_default_context()
    await aiosmtplib.send(
        message,
        hostname="127.0.0.1",
        port=1025)
        # username='',
        # password='',
        # use_tls=True


async def main():
    users_list = get_users()
    tasks = []
    for user in users_list:
        task = create_message(*user)
        tasks.append(task)
    messages = await asyncio.gather(*tasks)
    for message in messages:
        await send_message(message)


if __name__ == '__main__':
    asyncio.get_event_loop()
    asyncio.run(main(), debug=True)


# docker run -p 8025:8025 -p 1025:1025 mailhog/mailhog