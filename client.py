import time
import socket


class ClientError(Exception):
	pass


class Client:
	def __init__(self, H, P, timeout = None):
		self.H = H
		self.P = P
		self.timeout = timeout
		if timeout is not None:
			socket.setdefaulttimeout(self.timeout)

	def get(self, metr):

		try:
			s = socket.create_connection((self.H, self.P))  # Подключение к серверу
		except socket.error as err:
			raise ClientError("error with connection", err)
		Input = "get {}\n".format(metr)  # Форматируем данные которые ввел пользователь
		s.send(Input.encode("utf-8"))  # Отправляем данные на сервер
		Inf = ""  # Ответ от сервера
		while True:
			Inf += s.recv(4096).decode("utf-8")  # Получаем ответ от сервера
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
			s = socket.create_connection((self.H, self.P))
			Input = "put {} {} {}\n".format(metr, values, timestamp)
			s.send(Input.encode("utf-8"))
		else:
			s = socket.create_connection((self.H, self.P))
			Input = "put {} {} {}\n".format(metr, values, timestamp)
			s.send(Input.encode("utf-8"))


			Inf = s.recv(4096).decode("utf-8")
			if Inf == "ok\n\n":
				return 0
			else:
				raise ClientError(Inf)




