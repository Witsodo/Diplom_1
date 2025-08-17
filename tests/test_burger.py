import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


def test_set_buns():

    mock_bun = Mock()
    burger = Burger()
    burger.set_buns(mock_bun)
    assert burger.bun == mock_bun

def test_add_ingredient():

    mock_ingredients = Mock()
    burger = Burger()
    burger.add_ingredient(mock_ingredients)
    assert burger.ingredients == [mock_ingredients]

def test_remove_ingredient():

    burger = Burger()
    first_ingredient = Mock()
    second_ingredient = Mock()
    burger.add_ingredient(first_ingredient)
    burger.add_ingredient(second_ingredient)
    burger.remove_ingredient(0)
    assert first_ingredient not in burger.ingredients

def test_move_ingredient():

    burger = Burger()
    first_ingredient = Mock()
    second_ingredient = Mock()
    burger.add_ingredient(first_ingredient)
    burger.add_ingredient(second_ingredient)
    burger.move_ingredient(0,1)
    assert burger.ingredients == [second_ingredient, first_ingredient]

@pytest.mark.parametrize("bun_price, ingredient_price, exp_price",[
    (100, [], 200), #только булка
    (100, [10], 210), #булка и инг
    (0,[0,0],0), # бесплатно
    (100,[10,15],225), #булка, 2 инг
])
def test_get_price(bun_price, ingredient_price, exp_price):

    burger = Burger()
    mock_bun = Mock()
    mock_bun.get_price.return_value = bun_price
    burger.set_buns(mock_bun)

    for price in ingredient_price:
        mock_ingredient = Mock()
        mock_ingredient.get_price.return_value = price
        burger.add_ingredient(mock_ingredient)

    assert burger.get_price() == exp_price

def test_get_receipt():
    mock_bun = Mock()
    mock_bun.get_name.return_value = "Булка"
    mock_bun.get_price.return_value = 100

    sauce = Mock()
    sauce.get_name.return_value = "Вкусный"
    sauce.get_type.return_value = "SAUCE"
    sauce.get_price.return_value = 10

    filling = Mock()
    filling.get_name.return_value = "Начинка"
    filling.get_price.return_value = 15
    filling.get_type.return_value = "FILLING"

    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)

    expected_receipt = "\n".join([
        f"(==== Булка ====)",
        "= sauce Вкусный =",
        "= filling Начинка =",
        f"(==== Булка ====)\n",
        f"Price: {burger.get_price()}"
    ])

    assert burger.get_receipt() == expected_receipt
