import time
import socket


class ClientError(Exception):
	pass


class Client:
	def __init__(self, H, P, timeout = None):
		self.H = H
		self.P = P
		self.timeout = timeout
		self.sock = socket.socket()
		if timeout is not None:
			socket.setdefaulttimeout(self.timeout)

	def get(self, metr):
		self.sock.create_connection((self.H, self.P))  # Подключение к серверу
		Input = "get {}\n".format(metr)  # Форматируем данные которые ввел пользователь
		self.sock.send(Input.encode("utf-8"))  # Отправляем данные на сервер
		Inf = ""  # Ответ от сервера
		while True:
			Inf += self.sock.recv(4096).decode("utf-8")  # Получаем ответ от сервера
			if len(Inf) < 2:
				break
			elif Inf[-2] == "\n" == Inf[-1]:
				break
		if len(Inf) < 3 or Inf[:3] != "ok\n":
			raise ClientError(Inf)
		else:
			Inf = Inf.split("\n")  # Исключаем ok и последний пустой элемент
			Inf = Inf[1:]
			out_put = {} # Пустой словарь результатов
			for Input in Inf:
				if Input == "":
					continue
				metr, values, timestamp = Input.split()
				values = float(values)
				timestamp = int(timestamp)
				out_put.setdefault(metr, []).append((timestamp, values))  # Берем значения по ключу
			return out_put

	def put(self, metr, values, timestamp = None):
		if timestamp is None:
			timestamp = str(int(time.time()))
			self.sock.create_connection((self.H, self.P))
			Input = "put {} {} {}\n".format(metr, values, timestamp)
			self.sock.send(Input.encode("utf-8"))

			Inf = self.sock.recv(4096).decode("utf-8")
			if Inf == "ok\n\n":
				return 0
			else:
				raise ClientError(Inf)



