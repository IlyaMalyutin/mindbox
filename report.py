import pandas as pd
import numpy as np


def get_most_common_products(order_lines, n_products):
    """
    Выберем наиболее популярные продукты.
    Стоит отметить, что можно по разному выбрать "самые популярные продукты".
    Допустим, несколько product_id могут встречаться одинаковое колличество раз, на границе нашего n_products:

    product_id, n
    1, 10
    2, 9
    3, 8
    4, 8

    при n_products = 3 мы теряем в отчете 4-й продукт с тем же колличеством.
    Поэтому я бы выбрал нижнюю границу встречаемости и взял все товары встречающиеся с ней и чаще.

    :param order_lines: pd.DataFrame
    :param n_products: int
    :return: list
    """
    value_counts = order_lines.ProductId.value_counts()
    counts_border = value_counts.iloc[n_products - 1]
    return value_counts[value_counts >= counts_border].index.tolist()


def get_orders_amount(order_lines):
    """
    Сумма по заказам
    :param order_lines: pd.DataFrame
    :return:
    """
    order_amount = order_lines.groupby('OrderId', as_index=False).sum()
    order_amount.rename(columns={'Price': 'OrderAmount'}, inplace=True)
    return order_amount[['OrderId', 'OrderAmount']]


def report_most_common_products(orders, order_lines, order_time_gte, order_time_lte, n_products):
    """
    --------
    Задание:
        Постройте отчёт по популярным продуктами - функцию, возвращающую pandas.DataFrame, где видны
            * самые популярные за последний месяц продукты
            * суммарная выручка по каждому такому продукту
            * средний чек заказов, в которых есть такие продукты
    --------
    "за последний месяц" - неточная формулировка, за текущий месяц, за последние 30 дней или за прошлый месяц,
    поэтому отчет сделал универсальным за любые [order_time_gte, order_time_lte].

    Вряд ли вызов реального метода был бы с такой же сигнатурой,
    скорее всего эффективнее будет агрегировать orders и order_lines в базе данных
    и забирать только нужные n_products (число наиболее поплярных продуктов).
    Отдельно уточнил бы, что считается мерой популярности продукта: число единиц или число чеков с ним?
    По умолчанию буду считать число единиц.


    :param orders: pd.DataFrame
    :param order_lines: pd.DataFrame
    :param order_time_gte: datetime
    :param order_time_lte: datetime
    :param n_products: int
    :return: pd.DataFrame
    """
    order_ids = orders[(orders.DateTime >= order_time_gte) & (orders.DateTime <= order_time_lte)].OrderId

    """фильтрация по заказам, за нужные даты"""
    order_lines = order_lines[order_lines.OrderId.isin(order_ids)]
    """добавляем инфу по суммам заказов..."""
    order_lines = order_lines.merge(get_orders_amount(order_lines.copy()), on='OrderId')
    """...что бы при фильтрация по топу продуктов, не потерять ее"""
    order_lines = order_lines[order_lines.ProductId.isin(get_most_common_products(order_lines, n_products))]

    return order_lines.groupby('ProductId', as_index=False).agg({'OrderAmount': np.mean, 'Price': np.sum}).rename(
        columns={'Price': 'ProductAmount', 'OrderAmount': 'MeanOrderAmount'})
