<!-- Simple Python socket chat -->
# Проектное задание:
*  Список пользователей чата
*  Пользователи общаются друг с другом
*  Сервер отправляет сообщение со списком пользователей для общения на выбор
*  Описать и оформить код (главное - комментарии и аккуратность)

# Структура проектного задания:
1) Описание работы: в чём задание, что использовалось, как работает, на чём основано, какие технологии используются 
2) Теоретическая часть: подробная теоретическая сводка по предыдущему пункту 
3) Практическая часть: ваш код с описаниями блоков. что в нём происходит, как это работает, зачем это нужно
4) Скриншоты работы в разных ситуациях
5) Выводы 

<!-- DESCRIPTION -->
## 1. Описание работы проекта
Задание состоит в создании чата в которм пользователи могут подключаться и общаться как со всеми так и отправлять сообщения определенным клиентам.
В проекте есть сервер, который обрабатывает запросы от клиентов и является связующим звеном. Сервер работает с технической частью, переводит запросы клиентов в техническую информацию. Задача клиента сводится к отправке и получению сообщений и не более.

Для работы проекта использовались модули <b>Socket</b> и <b>Threading</b>. <b>Socket</b> это низкоуровневый сетевой интерфейс, он позволяет серверному сокету прослушивает определенный порт, а клиентскому подключается к серверу. Модуль <b>Threading</b> значительно упрощает работу с потоками и позволяет программировать запуск нескольких операций одновременно, это позволит серверу принимать все входящие подключения и сообщения, а клиентам принимать и отправлять сообщения. Без модуля все бы шло "лесенкой" делая работу проекта невозможной.

### Установка

1. Для начала клонируем репозиторий:
   ```sh
   git clone https://github.com/meligera/chat_chat.git
   ```
2. Переходим в папку с проектом: 
    ```sh
   cd chat_chat
   ```
3. Запускаем сервер коммандой:
    ```sh
   python server.py
   ```
4. Теперь можем принимать подключения от клиентов:
    ```sh
   python client.py
   ```

## 2. Теоретическая часть
Прицип работы <b>TCP Socket:</b>
<div align="left">
<a href="https://ibb.co/jRs9NRn"><img src="https://i.ibb.co/k1vV71N/v2.png" alt="v2" border="0"></a>
</div>

<hr>

В программировании конкуренция (от англ. concurrent - одновременный) - это одновременное выполнение разных задач (потоков, процессов).
Зачастую нам хочется распараллелить выполнение задач по одной из множества причин, например:

1) Ограничения ввода-вывода (процессы выполняются быстрее, чем работа с памятью, дисками, сетями и т.д.)
2) Ограничения процессора (сложные вычисления, трудоемкие процессы)
3) Последовательность или синхронность задач. (одни выполняются быстрее, другие медленнее)
4) Асинхронность задач (задачи выполняются независимо и нужно упорядочить их выполнение)

Базовое понятие <b>потоков</b>:
* Потоки работают внутри процесса, разделяя между собой
физические ресурсы процессора.
* В Python для этого есть модуль <b>Threading</b>, который использует
потоки, а не процессы. Threading (от англ. thread - нить, жила)

## 3. Практическая часть
### Серверная часть

```sh
# Импортирование модулей
import threading
import socket

# Функция отправки сообщений всем
def broadcast()
       
# Функция отправки определенному пользователю
def send()

# Функция обработки команд от клиента, если команды нет то происходит пересылка сообщения всем пользователям
def handle()

# Главная функция производящая авторизацию и начинающую поток с каждым подключением
def recieve()

# Вызов потока в функции recieve()
thread = threading.Thread(target=handle, args=(client,))
thread.start()

# Отправка отформатированного сообщения
def whisper()

#  Основной модуль вызова программы
if __name__ == '__main__'
```
### Клиентская часть
```sh
# Импортирование модулей
import threading
import socket

# Функция приема сообщений
def recieve()

#  Функция отправки сообщений
def write()

# Запуск две функции в потоке
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
```
