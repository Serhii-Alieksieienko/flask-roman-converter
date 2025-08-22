# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def number_to_roman(number):
    """
    Convert an integer to Roman numeral representation.
    
    Args:
        number: Integer between 1 and 3999
        
    Returns:
        String representation of the Roman numeral
        
    Raises:
        ValueError: If number is not between 1 and 3999
    """
    number = int(number)
    if not 0 < number < 4000:
        raise ValueError("Input must be an integer between 1 and 3999")

    roman_map = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]

    roman = ""
    for value, numeral in roman_map:
        count, number = divmod(number, value)
        roman += numeral * count
    return roman


def roman_to_number(roman):
    """
    Convert a Roman numeral to integer representation.
    
    Args:
        roman: String representation of Roman numeral
        
    Returns:
        Integer value of the Roman numeral
        
    Raises:
        ValueError: If input is not a valid Roman numeral
    """
    if not roman or not isinstance(roman, str):
        raise ValueError("Input must be a non-empty string")
    
    roman = roman.upper()
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    # Validate characters
    for char in roman:
        if char not in roman_values:
            raise ValueError(f"Invalid Roman numeral character: {char}")
    
    total = 0
    prev_value = 0
    
    for char in reversed(roman):
        value = roman_values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    
    # Validate the result by converting back
    if number_to_roman(total) != roman:
        raise ValueError(f"Invalid Roman numeral format: {roman}")
    
    return total