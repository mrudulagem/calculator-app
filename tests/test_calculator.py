import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from src.calculator import add, subtract, multiply, divide, power, factorial, fibonacci


# --- add ---

def test_add_two_positive_integers():
    assert add(2, 3) == 5

def test_add_positive_and_negative():
    assert add(10, -4) == 6

def test_add_two_negatives():
    assert add(-3, -7) == -10

def test_add_with_zero():
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_zeros():
    assert add(0, 0) == 0

def test_add_floats():
    assert add(1.5, 2.5) == pytest.approx(4.0)

def test_add_large_numbers():
    assert add(10**9, 10**9) == 2 * 10**9

def test_add_strings_concatenates():
    assert add("foo", "bar") == "foobar"


# --- subtract ---

def test_subtract_two_positives():
    assert subtract(10, 3) == 7

def test_subtract_result_negative():
    assert subtract(3, 10) == -7

def test_subtract_same_values():
    assert subtract(5, 5) == 0

def test_subtract_with_zero():
    assert subtract(7, 0) == 7
    assert subtract(0, 7) == -7

def test_subtract_negatives():
    assert subtract(-4, -6) == 2

def test_subtract_floats():
    assert subtract(5.5, 2.2) == pytest.approx(3.3)


# --- multiply ---

def test_multiply_two_positives():
    assert multiply(3, 4) == 12

def test_multiply_by_zero():
    assert multiply(99, 0) == 0
    assert multiply(0, 99) == 0

def test_multiply_by_one():
    assert multiply(7, 1) == 7

def test_multiply_two_negatives():
    assert multiply(-3, -4) == 12

def test_multiply_positive_and_negative():
    assert multiply(5, -3) == -15

def test_multiply_floats():
    assert multiply(2.5, 4.0) == pytest.approx(10.0)

def test_multiply_large_numbers():
    assert multiply(10**6, 10**6) == 10**12


# --- divide ---

def test_divide_exact():
    assert divide(10, 2) == 5.0

def test_divide_returns_float():
    assert divide(7, 2) == pytest.approx(3.5)

def test_divide_negative_numerator():
    assert divide(-9, 3) == pytest.approx(-3.0)

def test_divide_negative_denominator():
    assert divide(9, -3) == pytest.approx(-3.0)

def test_divide_both_negative():
    assert divide(-8, -4) == pytest.approx(2.0)

def test_divide_numerator_zero():
    assert divide(0, 5) == 0.0

def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_by_zero_with_negative_numerator_raises():
    with pytest.raises(ValueError):
        divide(-5, 0)

def test_divide_floats():
    assert divide(5.0, 2.0) == pytest.approx(2.5)


# --- power ---

def test_power_positive_exponent():
    assert power(2, 10) == 1024

def test_power_exponent_zero():
    assert power(99, 0) == 1

def test_power_exponent_one():
    assert power(7, 1) == 7

def test_power_base_zero():
    assert power(0, 5) == 0

def test_power_base_zero_exponent_zero():
    assert power(0, 0) == 1

def test_power_negative_base_even_exponent():
    assert power(-2, 4) == 16

def test_power_negative_base_odd_exponent():
    assert power(-2, 3) == -8

def test_power_negative_exponent_returns_fraction():
    assert power(2, -1) == pytest.approx(0.5)

def test_power_float_base():
    assert power(2.0, 3) == pytest.approx(8.0)

def test_power_large():
    assert power(10, 6) == 1_000_000


# --- factorial ---

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_one():
    assert factorial(1) == 1

def test_factorial_small():
    assert factorial(5) == 120

def test_factorial_larger():
    assert factorial(10) == 3628800

def test_factorial_two():
    assert factorial(2) == 2

def test_factorial_three():
    assert factorial(3) == 6

def test_factorial_negative_raises():
    with pytest.raises(ValueError, match="Cannot compute factorial of a negative number"):
        factorial(-1)

def test_factorial_large_negative_raises():
    with pytest.raises(ValueError):
        factorial(-100)

def test_factorial_large_value():
    assert factorial(20) == 2432902008176640000


# --- fibonacci ---

def test_fibonacci_zero():
    assert fibonacci(0) == 0

def test_fibonacci_one():
    assert fibonacci(1) == 1

def test_fibonacci_two():
    assert fibonacci(2) == 1

def test_fibonacci_three():
    assert fibonacci(3) == 2

def test_fibonacci_ten():
    assert fibonacci(10) == 55

def test_fibonacci_sequence_values():
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    for i, val in enumerate(expected):
        assert fibonacci(i) == val

def test_fibonacci_negative_raises():
    with pytest.raises(ValueError, match="Cannot compute Fibonacci of a negative number"):
        fibonacci(-1)

def test_fibonacci_large_negative_raises():
    with pytest.raises(ValueError):
        fibonacci(-50)

def test_fibonacci_large():
    assert fibonacci(20) == 6765

def test_fibonacci_thirty():
    assert fibonacci(30) == 832040