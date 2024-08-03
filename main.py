import multiprocessing


class WarehouseManager:
    def __init__(self):
        self.data = multiprocessing.Manager().dict()  # Используем менеджер для обеспечения многопроцессорности

    def process_request(self, request):
        product, action, quantity = request

        if action == "receipt":
            # Если продукт уже существует, увеличиваем его количество, иначе добавляем с начальным количеством
            if product in self.data:
                self.data[product] += quantity
            else:
                self.data[product] = quantity
        elif action == "shipment":
            # Уменьшаем количество товара при отгрузке, если он есть в наличии
            if product in self.data and self.data[product] > 0:
                self.data[product] = max(self.data[product] - quantity, 0)

    def run(self, requests):
        processes = []
        for request in requests:
            p = multiprocessing.Process(target=self.process_request, args=(request,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()


# Пример работы
if __name__ == "__main__":
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(dict(manager.data))  # Преобразуем в обычный словарь для отображения