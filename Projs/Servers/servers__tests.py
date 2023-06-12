#!/usr/bin/python
# -*- coding: utf-8 -*-
# 8: Wieloch (303080), Rybska (401417), Sukiennik (401060)

import unittest
from collections import Counter

from servers_skeleton import ListServer, Product, Client, MapServer, TooManyProductsFoundError, Server

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_is_sorted1(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('RRR23', 3), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(([products[3], products[1]]), entries)

    def test_get_entries_is_sorted2(self):
        products = [Product('PP234', 8), Product('RR23', 7), Product('PP235', 6)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(([products[2], products[1], products[0]]), entries)

    def test_get_entries_is_sorted3(self):
        products = [Product('PP234', 6), Product('RR23', 7), Product('PP235', 8)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(([products[0], products[1], products[2]]), entries)

    def test_get_entries_is_sorted4(self):
        products = [Product('PPP234', 6), Product('PRR23', 6), Product('PPP235', 6)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(3)
            self.assertEqual(([products[0], products[1], products[2]]), entries)

    def test_get_entries_too_many_products_error1(self):
        products = [Product('PC12', 1), Product('PP234', 2), Product('PP235', 3), Product('PP211', 5), Product('PA238', 4)]
        with self.assertRaises(TooManyProductsFoundError) as actual:
            for server_type in server_types:
                server = server_type(products)
                entries = server.get_entries(2)
        expected = TooManyProductsFoundError(len(products), Server.n_max_returned_entries)
        self.assertEqual(expected.args[0], actual.exception.args[0])

    def test_get_entries_too_many_products_error2(self):
        products = [Product('C12', 6), Product('A234', 8), Product('F25', 9), Product('G11', 3)]
        with self.assertRaises(TooManyProductsFoundError) as actual:
            for server_type in server_types:
                server = server_type(products)
                entries = server.get_entries(1)
        expected = TooManyProductsFoundError(len(products), Server.n_max_returned_entries)
        self.assertEqual(expected.args[0], actual.exception.args[0])

    def test_get_entries_too_many_products_pass(self):
        products = [Product('C12', 6), Product('A234', 8), Product('F25', 9)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(1)
            expected = [products[0], products[1], products[2]]
            self.assertEqual(expected, entries)


class ClientTest(unittest.TestCase):

    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_empty_list(self):
        products = [Product('C12', 6), Product('ACVB234', 8), Product('FAS25', 9), Product('G11', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_too_many_products_error(self):
        products = [Product('C12', 6), Product('A234', 8), Product('F25', 9), Product('G11', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(1))

    def test_is_right_product_name1(self):
        with self.assertRaises(ValueError) as actual:
            products = [Product('234', 2)]
        expected = ValueError('Product name has to have minimum one letter and minimum one digit')
        self.assertEqual(expected.args[0], actual.exception.args[0])

    def test_is_right_product_name2(self):
        with self.assertRaises(ValueError) as actual:
            products = [Product('AB', 4)]
        expected = ValueError('Product name has to have minimum one letter and minimum one digit')
        self.assertEqual(expected.args[0], actual.exception.args[0])

    def test_is_right_product_name3(self):
        with self.assertRaises(ValueError) as actual:
            products = [Product('123AB', 7)]
        expected = ValueError('Product name format is <letters><digits>')
        self.assertEqual(expected.args[0], actual.exception.args[0])


if __name__ == '__main__':
    unittest.main()
    
# 8: Wieloch (303080), Rybska (401417), Sukiennik (401060)
