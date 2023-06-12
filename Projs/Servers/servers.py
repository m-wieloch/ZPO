#!/usr/bin/python
# -*- coding: utf-8 -*-
# 8: Wieloch (303080), Rybska (401417), Sukiennik (401060)
import re
from typing import Optional, List, TypeVar, Union
from abc import ABC, abstractmethod


class Product:
    # DONE: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self._is_right_product_name()

    def __eq__(self, other):
        return self.name == other  # DONE: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))

    def _is_right_product_name(self):  # DONE
        # sprawdzanie - co najmniej jedną literę i co najmniej jedną cyfrę
        has_name_alphabet = False
        has_name_digit = False

        for char in self.name:
            if char.isalpha():
                has_name_alphabet = True
            if char.isdigit():
                has_name_digit = True

        if has_name_alphabet is not True or has_name_digit is not True:
            raise ValueError('Product name has to have minimum one letter and minimum one digit')

        else:
            # sprawdzanie <ciąg_liter><ciąg_cyfr>
            name_alphabet_end = False

            for char in self.name:
                if not name_alphabet_end:
                    if not char.isalpha():
                        name_alphabet_end = True

                if name_alphabet_end:
                    if not char.isdigit():
                        raise ValueError('Product name format is <letters><digits>')


class ServerError(Exception):
    # Klasa bazowa dla wyjątków z serwera
    def __init__(self, msg=None):
        super().__init__(msg)


class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, n, n_max_returned_entries):
        self.n_max_returned_entries = n_max_returned_entries
        self.n = n
        super().__init__(msg=f"Too many products found (can find {n_max_returned_entries}, found {n})")


# DONE: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: int = 1) -> Union[List[Product], TooManyProductsFoundError]:
        products = self._get_entries_inside(n_letters)

        if not products:
            return []

        if len(products) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError(len(products), Server.n_max_returned_entries)

        # sortowanie bąbelkowe - rosnąco
        products_sorted = products[:]

        for j in range(len(products)):

            for i in range(1, len(products) - j):

                if products_sorted[i - 1].price > products_sorted[i].price:
                    products_sorted[i - 1], products_sorted[i] = products_sorted[i], products_sorted[i - 1]

        return products_sorted

    @abstractmethod
    def _get_entries_inside(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError()


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products

    def _get_entries_inside(self, n_letters: int = 1) -> List[Product]:
        product_list = []

        for element in self.products:
            if re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), element.name):
                product_list.append(element)

        return product_list


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)

        products_dict = {}
        for element in products:
            products_dict[element.name] = element.price

        self.products = products_dict

    def _get_entries_inside(self, n_letters: int = 1) -> List[Product]:
        product_list = []

        for name in self.products:
            if re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), name):
                product_list.append(Product(name, self.products[name]))

        return product_list


# Zdefiniowana podpowiedź typu
ServerType = TypeVar('ServerType', bound=Server)


class Client:
    # DONE: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: ServerType):
        self.server = server

    def get_total_price(self, n_letters: Optional[int] = 1) -> Optional[float]:
        try:
            self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None

        if not self.server.get_entries(n_letters):
            return None

        total_price = 0

        for elem in self.server.get_entries(n_letters):
            total_price += elem.price

        return total_price


# 8: Wieloch (303080), Rybska (401417), Sukiennik (401060)
