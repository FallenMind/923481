import socket
import subprocess


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
        request = "start"
        client_socket.sendall(request.encode('utf-8'))
        print(f"Отправлено: {request}")

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Получено: {response}")

        # Симулируем выполнение задачи и запускаем .exe файл
        if response.startswith("Запуск .exe с параметром"):
            # Предположим, что сервер передает строку типа: "Запуск .exe с параметром program.exe param1 param2"
            command = response.split(" ", 1)[1]  # Получаем команду из ответа сервера

            # Запуск .exe файла с параметрами
            print(f"Запуск: {command}")
            try:
                result = subprocess.run(command, shell=True, check=True)
                # Если выполнение завершилось успешно
                client_socket.sendall(f"Задача выполнена: {command}".encode('utf-8'))
                print(f"Отправлено: Задача выполнена")
            except subprocess.CalledProcessError as e:
                # Если возникла ошибка при выполнении
                error_message = f"Ошибка при выполнении: {str(e)}"
                client_socket.sendall(error_message.encode('utf-8'))
                print(f"Отправлено: {error_message}")

    finally:
        # Закрываем соединение
        client_socket.close()


if __name__ == '__main__':
    client_program()
