import unittest
import pandas as pd

import report

orders_list = [
    {'OrderId': 1, 'CustomerId': 1, 'DateTime': '2017-01-01 15:03:17'},
    {'OrderId': 2, 'CustomerId': 2, 'DateTime': '2018-01-01 15:03:17'},
    {'OrderId': 3, 'CustomerId': 3, 'DateTime': '2018-01-02 15:03:17'},
    {'OrderId': 4, 'CustomerId': 2, 'DateTime': '2018-01-03 16:00:00'},
    {'OrderId': 5, 'CustomerId': 3, 'DateTime': '2018-01-04 17:00:01'},
]
order_lines_list = [
    {'ProductId': 1, 'OrderId': 1, 'Price': 100.},

    {'ProductId': 1, 'OrderId': 2, 'Price': 100.},
    {'ProductId': 2, 'OrderId': 2, 'Price': 200.},
    {'ProductId': 3, 'OrderId': 2, 'Price': 300.},

    {'ProductId': 1, 'OrderId': 3, 'Price': 100.},
    {'ProductId': 3, 'OrderId': 3, 'Price': 300.},

    {'ProductId': 1, 'OrderId': 4, 'Price': 100.},
    {'ProductId': 2, 'OrderId': 4, 'Price': 200.},

    {'ProductId': 1, 'OrderId': 5, 'Price': 100.},
    {'ProductId': 2, 'OrderId': 5, 'Price': 200.},
    {'ProductId': 3, 'OrderId': 5, 'Price': 300.},
]


class ProductTest(unittest.TestCase):

    def setUp(self):
        self.orders = pd.DataFrame(orders_list)
        self.order_lines = pd.DataFrame(order_lines_list)

    def test_get_most_common_products(self):
        """
        Тестируется выбора популярных продуктов
        :return:
        """
        # тест вернет 'ProductId': 1, как самый популярный
        self.assertEqual([1], report.get_most_common_products(self.order_lines, n_products=1))

        # тест вернет 'ProductId': 1, 2, 3, так как у 2, 3 одинаковая встречаемость
        self.assertEqual([1, 2, 3], sorted(report.get_most_common_products(self.order_lines, n_products=2)))

    def test_orders_amount(self):
        """
        Тест подсчета суммы по заказам
        :return:
        """
        orders_amount = report.get_orders_amount(self.order_lines)
        self.assertEqual(5, orders_amount.shape[0])

        cases = [[1, 100], [2, 600], [3, 400], [4, 300], [5, 600]]
        for order_id, amount in cases:
            self.assertEqual(amount, orders_amount[orders_amount.OrderId == order_id].iloc[0].OrderAmount)

    def test_report_most_common_products_all(self):
        result = report.report_most_common_products(
            orders=self.orders,
            order_lines=self.order_lines,
            order_time_gte='2017-01-01 15:03:17',
            order_time_lte='2018-01-04 17:00:01',
            n_products=2
        )
        cases = [
            [1, 2000 / 5, 5 * 100],
            [2, 1500 / 3, 3 * 200],
            [3, 1600 / 3, 3 * 300],
        ]
        for product_id, mean_order, amount in cases:
            _report = result[result.ProductId == product_id]
            self.assertEqual(mean_order, _report.iloc[0].MeanOrderAmount, product_id)
            self.assertEqual(amount, _report.iloc[0].ProductAmount, product_id)

    def test_report_most_common_products_one(self):
        result = report.report_most_common_products(
            orders=self.orders,
            order_lines=self.order_lines,
            order_time_gte='2017-01-01 15:03:17',
            order_time_lte='2018-01-04 17:00:01',
            n_products=1
        )
        cases = [
            [1, 1900 / 5, 5 * 100],
        ]
        print(result)
        for product_id, mean_order, amount in cases:
            _report = result[result.ProductId == product_id]
            self.assertEqual(mean_order, _report.iloc[0].MeanOrderAmount, product_id)
            self.assertEqual(amount, _report.iloc[0].ProductAmount, product_id)


    def test_report_most_common_products_one_date_filter(self):
        result = report.report_most_common_products(
            orders=self.orders,
            order_lines=self.order_lines,
            order_time_gte='2018-01-01 15:03:17',
            order_time_lte='2018-01-04 17:00:01',
            n_products=1
        )
        cases = [
            [1, 1900 / 4, 4 * 100],
        ]
        for product_id, mean_order, amount in cases:
            _report = result[result.ProductId == product_id]
            self.assertEqual(mean_order, _report.iloc[0].MeanOrderAmount, product_id)
            self.assertEqual(amount, _report.iloc[0].ProductAmount, product_id)


if __name__ == '__main__':
    unittest.main()


