"""
Unit tests for calculator application
"""
import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import add, subtract, multiply, divide, Calculator


class TestBasicOperations:
    """Test basic calculator functions"""

    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(10, 10) == 0

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 5) == -10
        assert multiply(0, 100) == 0

    def test_divide(self):
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)


class TestCalculatorClass:
    """Test Calculator class functionality"""

    def test_calculator_init(self):
        calc = Calculator("TestCalc")
        assert calc.name == "TestCalc"
        assert calc.history == []

    def test_calculator_add(self):
        calc = Calculator("TestCalc")
        result = calc.calculate("add", 5, 3)
        assert result == 8
        assert len(calc.history) == 1

    def test_calculator_history(self):
        calc = Calculator("TestCalc")
        calc.calculate("add", 10, 5)
        calc.calculate("multiply", 3, 4)

        history = calc.get_history()
        assert len(history) == 2
        assert history[0]["operation"] == "add"
        assert history[0]["result"] == 15
        assert history[1]["operation"] == "multiply"
        assert history[1]["result"] == 12

    def test_calculator_invalid_operation(self):
        calc = Calculator("TestCalc")
        with pytest.raises(ValueError, match="Unknown operation"):
            calc.calculate("power", 2, 3)

    def test_calculator_divide_by_zero(self):
        calc = Calculator("TestCalc")
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.calculate("divide", 10, 0)
