import asyncio

class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.addr = writer.get_extra_info('peername')

    async def handle(self):
        print(f"Connection from {self.addr}")

        try:
            while True:
                try:
                    # Ожидаем ответ от клиента в течение 30 минут (1800 секунд)
                    data = await asyncio.wait_for(self.reader.read(100), timeout=1800)
                    if not data:
                        break

                    message = data.decode()
                    print(f"Received from {self.addr}: {message}")

                    response = f"Echo: {message}"
                    self.writer.write(response.encode())
                    await self.writer.drain()
                except asyncio.TimeoutError:
                    # Если прошло 30 минут без ответа
                    print(f"No response from {self.addr} within 30 minutes. Performing alternative action.")
                    await self.handle_timeout()
                    break

        except asyncio.CancelledError:
            print(f"Connection closed by {self.addr}")
        finally:
            self.close()

    async def handle_timeout(self):
        # Действие, которое нужно выполнить, если клиент не отвечает
        print(f"Performing timeout action for {self.addr}")
        # Например, отправим сообщение клиенту о таймауте
        message = "Timeout: No response received in 30 minutes."
        self.writer.write(message.encode())
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
