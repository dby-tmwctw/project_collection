"""
QR Code Generator
"""

import comp140_module5 as qrcode
import comp140_module5_z256 as z256

def divide_terms(coefficient1, power1, coefficient2, power2):
    """
    Divide the first term, coefficient1*x^power1, by the
    second term, coefficient2*x^power2. This method requires
    that coefficient2 <= coefficient1.

    Returns an instance of a Polynomial representing the resulting
    term.
    """
    # From recipe: (a*x^b) / (c*x^d) = (a/c) * x^(b-d)
    new_coeff = z256.div(coefficient1, coefficient2)
    new_pow = power1 - power2

    # Represent our answer as a Polynomial
    divided = Polynomial()
    divided = divided.add_term(new_coeff, new_pow)
    return divided

def get_powers_sequence(original_map):
    """
    Get an input map corresponding to a polynomial, return a sequence
    with all effective powers (powers with non-zero coefficient) in
    descending order
    """
    return_sequence = []
    # Add power to return_sequence only if the value mapped to it is not 0
    for original_key in original_map.keys():
        if original_map[original_key] != 0:
            return_sequence.append(original_key)
    return_sequence.sort(reverse=True)
    return return_sequence

class Polynomial:
    """
    A class used to abstract methods on a polynomial in the finite
    field Z_256 (including numbers from 0 through 255).

    Since 256 is not prime, but is rather of the form p^n = 2^8, this
    representation uses special arithmetic via the z256 module so as to
    preserve multiplicative inverses (division) inside this field.
    """

    def __init__(self, terms=None):
        """
        Creates a new Polynomial object.  If a dictionary of terms, mapping
        powers to coefficients, is provided, they will be the terms of
        the polynomial, otherwise the polynomial will be the 0
        polynomial.
        """
        if terms != None:
            self._terms = dict(terms)
        else:
            self._terms = {}

    def __str__(self):
        """
        Returns a string representation of the polynomial, containing the
        class name and all of the terms.
        """
        # Create a string of the form "ax^n + bx^n-1 + ... + c" by
        # creating a string representation of each term, and inserting
        # " + " in between each
        term_strings = []

        # Add the highest powers first
        powers = list(self._terms.keys())
        powers.sort(reverse=True)
        for power in powers:
            coefficient = self._terms[power]
            # Don't print out terms with a zero coefficient
            if coefficient != 0:
                # Don't print "x^0"; that just means it's a constant
                if power == 0:
                    term_strings.append("%d" % coefficient)
                else:
                    term_strings.append("%d*x^%d" % (coefficient, power))

        terms_str = " + ".join(term_strings)
        if terms_str == "":
            terms_str = "0"
        return "Polynomial: %s" % terms_str

    def __eq__(self, other_polynomial):
        """
        Return True if other_polynomial contains the same terms
        as self, False otherwise.
        """
        # Make sure that other_polynomial is a Polynomial
        if not isinstance(other_polynomial, Polynomial):
            return False

        # Get the terms of the other_polynomial
        terms = other_polynomial.get_terms()

        # Check that all terms in other_polynomial appear in self
        for power, coefficient in terms.items():
            if coefficient != 0:
                if not self._terms.has_key(power):
                    return False
                if self._terms[power] != coefficient:
                    return False

        # Check that all terms in self appear in other_polynomial
        for power, coefficient in self._terms.items():
            if coefficient != 0:
                if not terms.has_key(power):
                    return False
                if terms[power] != coefficient:
                    return False

        return True

    def __ne__(self, other_polynomial):
        """
        Return False if other_polynomial contains the same terms
        as self, True otherwise.
        """
        return not self.__eq__(other_polynomial)

    def get_terms(self):
        """
        Returns a dictionary of terms, mapping powers to coefficients.
        This dictionary is a completely new object and is not a reference
        to any internal structures.
        """
        terms = dict(self._terms)
        return terms

    def get_degree(self):
        """
        Returns the maximum power over all terms in this polynomial.
        """
        # Since we don't clean zero-coefficient powers out of our dictionary,
        # we need a trickier get_degree function, to take into account that
        # some coefficients could be zero.
        highest_power = 0
        for power in self._terms:
            if (power > highest_power) and (self._terms[power] != 0):
                highest_power = power

        return highest_power


    def get_coefficient(self, power):
        """
        Given a power of x, returns the coefficient of x^(power) in this
        polynomial. If there is no coefficient of x^(power), this method
        returns 0.
        """
        if power in self._terms:
            return self._terms[power]
        else:
            return 0

    def add_term(self, coefficient, power):
        """
        Returns a new Polynomial that is the sum of adding this polynomial
        to (coefficient) * x^(power) using Z_256 arithmetic to add
        coefficients, if necessary.
        """
        # Replace with your code for part 3.A
        # Make a new copy of the current dictionary
        new_expression = dict(self._terms)
        # Check whether the power exists in the polynomial and add
        # accordingly
        if power in self._terms.keys():
            original_coefficient = new_expression[power]
            new_expression[power] = z256.add(original_coefficient, coefficient)
        else:
            new_expression[power] = z256.add(0, coefficient)
        #print new_expression
        return Polynomial(new_expression)

    def subtract_term(self, coefficient, power):
        """
        Returns a new Polynomial that is the difference of this polynomial
        and (coefficient) * x^(power) using Z_256 arithmetic to subtract
        coefficients, if necessary.
        """
        # Replace with your code for part 3.B
        new_expression1 = Polynomial(self._terms)
        return new_expression1.add_term(z256.sub(0, coefficient), power)

    def multiply_by_term(self, coefficient, power):
        """
        Returns a new Polynomial that is the product of multiplying
        this polynomial by (coefficient) * x^(power).
        """
        # Replace with your code for part 3.C
        new_map = {}
        # Multiply each term in current polynomial by the new term, and
        # add them together
        for original_power, original_coefficient in self._terms.items():
            new_map[original_power + power] = z256.mul(original_coefficient, coefficient)
        return Polynomial(new_map)

    def add_polynomial(self, other_polynomial):
        """
        Returns a new Polynomial that is the sum of all terms in the
        current polynomial and all terms in the other_polynomial.
        """
        # Replace with your code for part 4.A
        add_map = other_polynomial.get_terms()
        intermediate = Polynomial(self._terms)
        # Add each term in new polynomial to the current polynoial
        for power, coefficient in add_map.items():
            intermediate = intermediate.add_term(coefficient, power)
        # The code below is to avoid creating polynomials with maps such as
        # {4:0}, which is effectively 0 but will cause trouble in the remainder
        # function
        zero_indicator = True
        for coefficient in intermediate.get_terms().values():
            if coefficient != 0:
                zero_indicator = False
        if zero_indicator:
            return Polynomial()
        else:
            return Polynomial(intermediate.get_terms())

    def subtract_polynomial(self, other_polynomial):
        """
        Returns a new Polynomial that is the difference of all terms
        in the current polynomial and all terms in the other_polynomial.
        """
        # Replace with your code for part 4.B
        add_map = other_polynomial.get_terms()
        intermediate = Polynomial(self._terms)
        # Subtract each terms away from current polynomial with
        # the subtract_term function
        for power, coefficient in add_map.items():
            intermediate = intermediate.subtract_term(coefficient, power)
        # The code below is to ensure that wo do not return polynomials with
        # value 0 but the map corresponding to it is not 0
        zero_indicator = True
        for coefficient in intermediate.get_terms().values():
            if coefficient != 0:
                zero_indicator = False
        if zero_indicator:
            return Polynomial()
        else:
            return Polynomial(intermediate.get_terms())

    def multiply_by_polynomial(self, other_polynomial):
        """
        Returns a new Polynomial that is the product of this
        polynomial and the provided other_polynomial.

        The returned polynomial is the sum of multiplying each term
        in this polynomial (self) by the other_polynomial.
        """
        # Replace with your code for part 4.C
        other_map = other_polynomial.get_terms()
        result_polynomial = Polynomial({})
        intermediate = Polynomial(self._terms)
        # Multiply current polynomial by each term in the other polynomial, and
        # add them together
        for power, coefficient in other_map.items():
            step_result = intermediate.multiply_by_term(coefficient, power)
            result_polynomial = result_polynomial.add_polynomial(step_result)
        return result_polynomial

    def remainder(self, denominator):
        """
        Returns a new Polynomial that is the remainder after dividing this
        polynomial by denominator.

        Note: does *not* return the quotient; only the remainder!

        """
        # Replace with your code for part 4.D
        if self._terms == {}:
            zero_polynomial = Polynomial()
            return zero_polynomial
        denominator_map = denominator.get_terms()
        remainder = Polynomial(self._terms)
        powers = get_powers_sequence(remainder.get_terms())
        highest_power = powers[0]
        powers_denominator = get_powers_sequence(denominator.get_terms())
        highest_power_denominator = powers_denominator[0]
        # Keep dividing highest term of the current polynomial by highest term
        # of denominator, then multiply denominator by the term get and subtract
        # the answer away from current polynomial, untill the highest power of
        # current polynomial less than the highest power of denominator
        while highest_power >= highest_power_denominator:
            remainder_map = remainder.get_terms()
            single_term = divide_terms(remainder_map[highest_power], highest_power, denominator_map[highest_power_denominator], highest_power_denominator)
            multiply_term = denominator.multiply_by_polynomial(single_term)
            remainder = remainder.subtract_polynomial(multiply_term)
            powers1 = get_powers_sequence(remainder.get_terms())
            if len(powers1) == 0:
                highest_power = 0
            else:
                highest_power = powers1[0]
            # The special case below is to avoid bug when the program try
            # to divide 0 by 0
            if highest_power == 0 and highest_power_denominator == 0:
                return remainder
        return remainder

def create_message_polynomial(message, num_correction_bytes):
    """
    Description: Creates the appropriate Polynomial to represent the
        given message. Relies on the number of error correction
        bytes (k). The message polynomial is of the form
        message[i]*x^(n+k-i-1) for each number/byte in the message.

    Inputs:
    message -- a list of numbers between 0-255 representing data
    num_correction_bytes -- number of error correction bytes to use

    Returns:
    A Polynomial with the appropriate terms to represent message for
    the specified level of error correction.
    """
    # Replace with your code for part 5.A
    message_map = {}
    # Generate the polynomial by mathematical formula
    for index in range(0, len(message)):
        coefficient = message[index]
        power = num_correction_bytes + len(message) - index - 1
        message_map[power] = coefficient
    message_polynomial = Polynomial(message_map)
    return message_polynomial

def create_generator_polynomial(num_correction_bytes):
    """
    Description: Generates a static generator Polynomial for error
        correction, which is the product of (x-2^i) for all i in the
        set {0, 1, ..., num_correction_bytes - 1}.

    Inputs:
    num_correction_bytes -- desired number of error correction bytes.
        In the formula, this is represented as k.

    Returns:
    A generator Polynomial for generating Reed-Solomon encoding data.
    """
    # Replace with your code for part 5.B
    starting_map = {}
    starting_map[0] = z256.power(2, 0)
    starting_map[1] = 1
    generator_polynomial = Polynomial(starting_map)
    # The code below is to continue multiplying when k > 1
    if num_correction_bytes > 1:
        for power in range(1, num_correction_bytes):
            new_map = {}
            new_map[0] = z256.sub(0, z256.power(2, power))
            new_map[1] = 1
            new_expression = Polynomial(new_map)
            generator_polynomial = generator_polynomial.multiply_by_polynomial(new_expression)
    return generator_polynomial

def reed_solomon_correction(encoded_data, num_correction_bytes):
    """
    Takes a list of bytes (as numbers between 0-255) representing an
    encoded QR message.

    Returns a polynomial that represents the Reed-Solomon error
    correction code for the input data.
    """
    # Replace with your code for part 5.C
    message = create_message_polynomial(encoded_data, num_correction_bytes)
    generator = create_generator_polynomial(num_correction_bytes)
    remainder = message.remainder(generator)
    return remainder

# Uncomment the following line when you are ready to generate an
# actual QR code.  To do so, you must enter a short message in the
# "info" text box and hit return (be sure to hit return!).  You then
# must push the "Generate!" button.  This will generate a QR code for
# you to view - try scanning it with your phone!  If you would like to
# save your QR codes, you can use the "Image in a New Window" button
# to create a .png file that you can save by right clicking in your
# browser window.

# qrcode.start(reed_solomon_correction)
