import socket


def client_program():
    # Создаем сокет TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Определяем адрес и порт сервера
    host = '127.0.0.1'  # Локальный сервер, можно заменить на нужный IP-адрес
    port = 12345  # Порт, который использует сервер

    # Подключаемся к серверу
    client_socket.connect((host, port))

    try:
        # Отправляем запрос серверу
        request = "Запрос данных"
        client_socket.sendall(request.encode('utf-8'))
        print(f"Отправлено: {request}")

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Получено: {response}")

        # Симулируем выполнение задачи и отправляем уведомление
        if response == "Запрос получен, выполните задачу":
            print("Задача выполняется...")
            # Симуляция выполнения задачи
            result = "Задача выполнена"
            client_socket.sendall(result.encode('utf-8'))
            print(f"Отправлено: {result}")

    finally:
        # Закрываем соединение
        client_socket.close()


if __name__ == '__main__':
    client_program()
