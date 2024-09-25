import asyncio

class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.addr = writer.get_extra_info('peername')

    async def handle(self):
        print(f"Connection from {self.addr}")

        try:
            # Шаг 1: Ожидание сообщения о начале работы
            data = await self.reader.read(100)
            if not data:
                return

            message = data.decode().strip()
            print(f"Received from {self.addr}: {message}")

            if message.lower() == "start":
                # Шаг 2: Отправляем данные клиенту
                await self.send_data()

                # Шаг 3: Ждем ответа клиента в течение 30 минут
                await self.wait_for_response()
            else:
                print(f"Unexpected message from {self.addr}: {message}")

        except asyncio.CancelledError:
            print(f"Connection closed by {self.addr}")
        finally:
            self.close()

    async def send_data(self):
        # Здесь отправляем данные клиенту
        data_to_send = "Here is the data you requested."
        self.writer.write(data_to_send.encode())
        await self.writer.drain()
        print(f"Data sent to {self.addr}")

    async def wait_for_response(self):
        try:
            # Ожидаем ответ клиента в течение 30 минут
            data = await asyncio.wait_for(self.reader.read(100), timeout=1800)
            if data:
                response = data.decode().strip()
                print(f"Received response from {self.addr}: {response}")
            else:
                print(f"Client {self.addr} disconnected without response.")
        except asyncio.TimeoutError:
            # Если ответ не был получен в течение 30 минут
            print(f"No response from {self.addr} within 30 minutes. Performing alternative action.")
            await self.handle_timeout()

    async def handle_timeout(self):
        # Действие, если клиент не ответил
        timeout_message = "Timeout: No response received in 30 minutes."
        self.writer.write(timeout_message.encode())
        await self.writer.drain()

    def close(self):
        print(f"Closing connection from {self.addr}")
        self.writer.close()

clients = []  # Список всех клиентов

async def handle_client(reader, writer):
    client = Client(reader, writer)
    clients.append(client)  # Добавляем клиента в список
    await client.handle()
    clients.remove(client)  # Удаляем клиента из списка после завершения работы

async def main(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8888
    asyncio.run(main(host, port))