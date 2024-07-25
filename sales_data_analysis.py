import csv
import urllib.request
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


FILE_PATH = "https://raw.githubusercontent.com/anunuclse/Final_tesk_DE_step12/main/generated_data.csv"


# принимает путь к файлу и возвращает список продаж. 
# Продажи в свою очередь являются словарями с ключами product_name, quantity, price, date (название, количество, цена, дата).

def read_sales_data(FILE_PATH):
    # Загружаем CSV файл по URL
    response = urllib.request.urlopen(FILE_PATH)
    csv_data = response.read().decode('utf-8')
    
    # Используем io.StringIO для чтения данных из строки
    csvfile = io.StringIO(csv_data)
    sales_list = []

    # Чтение данных из CSV
    reader = csv.DictReader(csvfile)
    for row in reader:
        sales_list.append(row)
    
    return sales_list


#принимает список продаж и возвращает словарь, где ключ - название продукта, а значение - общая сумма продаж этого продукта.

def total_sales_per_product(sales_data):
    # Инициализация словаря для хранения сумм продаж по продуктам
    sales_summary_products = {}

    # Проход по списку продаж
    for sale in sales_data:
        product_name = sale['product_name']
        quantity = int(sale['quantity'])  # Преобразуем в целое число
        price = float(sale['price'])      # Преобразуем в число с плавающей точкой

        # Вычисление общей суммы для данного продукта
        total_sale = quantity * price

        # Обновление сумм в словаре
        if product_name in sales_summary_products:
            sales_summary_products[product_name] += total_sale
        else:
            sales_summary_products[product_name] = total_sale
    
    return sales_summary_products


# принимает список продаж и возвращает словарь, где ключ - дата, а значение общая сумма продаж за эту дату.

def sales_over_time(sales_data):
    # Инициализация словаря для хранения сумм продаж по датам
    sales_summary_dates = {}

    # Проход по списку продаж
    for sale in sales_data:
        product_name = sale['date']
        quantity = int(sale['quantity'])  # Преобразуем в целое число
        price = float(sale['price'])      # Преобразуем в число с плавающей точкой

        # Вычисление общей суммы для данного продукта
        total_sale = quantity * price

        # Обновление сумм в словаре
        if product_name in sales_summary_dates:
            sales_summary_dates[product_name] += total_sale
        else:
            sales_summary_dates[product_name] = total_sale
    
    return sales_summary_dates


def find_top_product_and_date(total_sales_per_product, sales_over_time):
    # Находим продукт с наибольшей выручкой
    top_product = max(total_sales_per_product, key=total_sales_per_product.get)
    top_revenue = total_sales_per_product[top_product]

    # Находим день с наибольшей суммой продаж
    top_day = max(sales_over_time, key=sales_over_time.get)
    top_sales = sales_over_time[top_day]
    
    print(f"Продукт, принесший наибольшую выручку: \"{top_product}\" с суммой продаж {top_revenue:.2f}")
    print(f"День, когда была наибольшая выручка: \"{top_day}\" с суммой продаж {top_sales:.2f}")

    return [top_product, top_revenue, top_day, top_sales]


def plot_sales(sales_by_product, sales_by_date, top_sales):
    # Сортировка данных по датам
    sorted_dates = sorted(sales_by_date.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
    sorted_sales_by_date = [sales_by_date[date] for date in sorted_dates]

    # Построение графика общей суммы продаж по продуктам
    plt.figure(figsize=(14, 8))
    
    plt.subplot(1, 2, 1)  # 1 строка, 2 столбца, 1-я ячейка
    plt.bar(sales_by_product.keys(), sales_by_product.values(), color='skyblue')
    plt.xlabel('Продукт')
    plt.ylabel('Общая сумма продаж')
    plt.title('Общая сумма продаж по продуктам')
    plt.xticks(rotation=45, ha='right')
    
    # Добавление текста над графиком
    plt.text(len(sales_by_product) - 1, max(sales_by_product.values()) * 1.1, 
             f'Продукт с наибольшей выручкой: "{top_sales[0]}"\nСумма продаж: {top_sales[1]:.2f}', 
             ha='right', va='bottom', fontsize=12, color='black')

    # Построение графика общей суммы продаж по дням
    plt.subplot(1, 2, 2)  # 1 строка, 2 столбца, 2-я ячейка
    plt.plot(sorted_dates, sorted_sales_by_date, marker='o', linestyle='-', color='orange')
    plt.xlabel('Дата')
    plt.ylabel('Общая сумма продаж')
    plt.title('Общая сумма продаж по дням')
    plt.xticks(rotation=45, ha='right')
    
    # Добавление текста над графиком
    plt.text(len(sorted_dates) - 1, max(sorted_sales_by_date) * 1.1, 
             f'День с наибольшей выручкой: "{top_sales[2]}"\nСумма продаж: {top_sales[3]:.2f}', 
             ha='right', va='bottom', fontsize=12, color='black')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sales_data = read_sales_data(FILE_PATH)
    sales_products = total_sales_per_product(sales_data)
    sales_dates = sales_over_time(sales_data)
    top_sales = find_top_product_and_date(sales_products, sales_dates)
    plot_sales(sales_products, sales_dates, top_sales)