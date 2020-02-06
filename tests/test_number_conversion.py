import pytest

from text2digits import text2digits


@pytest.mark.parametrize("input_text", [
    ('A random string'),
    ('Hello world. How are you?'),
])
def test_str_unchanged_if_no_numbers(input_text):
    t2d_default = text2digits.Text2Digits()
    result = t2d_default.convert(input_text)
    assert result == input_text  # unchanged


@pytest.mark.parametrize("input_text,expected", [
    ("one thousand six hundred sixty six", "1666"),
    ("one thousand and six hundred and sixty six", "1666"),
    ("ten thousand one", "10001"),
    ("ten thousand fifty", "10050"),
    ("ten thousand", "10000"),
    ("hundred thousand", "100000"),
    ("one hundred thousand", "100000"),
    ("fifty five thousand", "55000"),
    ("I am twenty nine", "I am 29"),
    ("I am thirty six years old with a child that is four. I would like to get him four cars!", "I am 36 years old with a child that is 4. I would like to get him 4 cars!"),
])
def test_positive_integers(input_text, expected):
    t2d_default = text2digits.Text2Digits()
    result = t2d_default.convert(input_text)
    assert result == expected


@pytest.mark.parametrize("input_text,expected", [
    ("I was born in twenty ten", "I was born in 2010"),
    ("I was born in nineteen sixty four", "I was born in 1964"),
    ("thirty twenty one", "3021"),
    ("sixteen sixty six", "1666"),
    ("twenty nineteen", "2019"),
    ("twenty twenty", "2020"),
    ("fifty one thirty three", "5133"),
    ("fifty five twelve", "5512"),
    ("thirty eleven", "3011"),
    ("sixty six ten", "6610"),
])
def test_years(input_text, expected):
    t2d_default = text2digits.Text2Digits()
    result = t2d_default.convert(input_text)
    assert result == expected


@pytest.mark.parametrize("input_text, expected", [
    ("it was twenty ten and was negative thirty seven degrees", "it was 2010 and was negative 37 degrees"),
    ("I was born in nineteen ninety two and am twenty six years old!", "I was born in 1992 and am 26 years old!"),
    ("asb is twenty two altogether fifty five twelve parrot", "asb is 22 altogether 5512 parrot"),
    ("twenty eleven zero three", "201103"),
])
def test_multiple_types_of_numbers(input_text, expected):
    t2d_default = text2digits.Text2Digits()
    result = t2d_default.convert(input_text)
    assert result == expected


@pytest.mark.parametrize("input_text,expected", [
    ("eleven hundred twelve", "1112"),
    ("Sixteen and seven", "16 and 7"),
    ("twenty ten and twenty one", "2010 and 21"),
    ("three forty five", "345"),
    ("nineteen", "19"),
    ("ninteen", "ninteen"),
    ("nintteen", "nintteen"),
    ("ninten", "ninten"),
    ("ninetin", "ninetin"),
    ("ninteen nineti niine", "ninteen nineti niine"),
    ("forty two,  two. 0.5-1", "42,  2. 0.1"),
    ("sixty six hundred", "6600"),
    ("one two zero three", "1203"),
    ("one fifty one twenty one", "15121"),
])
def test_others(input_text, expected):
    t2d_default = text2digits.Text2Digits()
    result = t2d_default.convert(input_text)
    assert result == expected


@pytest.mark.parametrize("ordinal_input,convert_ordinals,add_ordinal_ending,expected", [
    ('third', True, False, '3'),
    ('third', False, False, 'third'),
    ('third', True, True, '3rd'),
    # ordinal ending 'st'
    ('twenty-first', True, False, '21'),
    ('twenty-first', False, False, 'twenty-first'),
    ('twenty-first', True, True, '21st'),
    # ordinal ending 'nd'
    ('thirty-second', True, False, '32'),
    ('thirty-second', False, False, 'thirty-second'),
    ('thirty-second', True, True, '32nd'),
    # ordinal ending 'rd'
    ('forty-third', True, False, '43'),
    ('forty-third', False, False, 'forty-third'),
    ('forty-third', True, True, '43rd'),
    # ordinal ending 'th'
    ('fifty-fourth', True, False, '54'),
    ('fifty-fourth', False, False, 'fifty-fourth'),
    ('fifty-fourth', True, True, '54th'),
])
def test_ordinal_conversion_switch_disabled(ordinal_input, convert_ordinals, add_ordinal_ending, expected):

    input_str = "she was the {} to finish the race"
    t2d_default = text2digits.Text2Digits(convert_ordinals=convert_ordinals, add_ordinal_ending=add_ordinal_ending)
    result = t2d_default.convert(input_str.format(ordinal_input))
    assert result == input_str.format(expected)


@pytest.mark.parametrize("ordinal_input,convert_ordinals,add_ordinal_ending,expected", [
    ('eighth', True, False, '8'),
    ('eighth', False, False, 'eighth'),
    ('eighth', True, True, '8th'),
    ('ninety-seventh', True, False, '97'),
    ('ninety-seventh', False, False, 'ninety-seventh'),
    ('ninety-seventh', True, True, '97th'),
])
def test_ordinal_at_the_end_of_the_sentence(ordinal_input, convert_ordinals, add_ordinal_ending, expected):
    input_str = "she finished {}"
    t2d_default = text2digits.Text2Digits(convert_ordinals=convert_ordinals, add_ordinal_ending=add_ordinal_ending)
    result = t2d_default.convert(input_str.format(ordinal_input))
    assert result == input_str.format(expected)


def test_ordinal_multi_occurence_and_cardinal():
    # using two ordinal numbers with different endings ('th' and 'nd')
    # and a cardinal number in the middle
    input_str = "she finished sixty-fourth on race number six and he finished forty-second"
    t2d_default = text2digits.Text2Digits(convert_ordinals=True, add_ordinal_ending=True)
    result = t2d_default.convert(input_str)
    assert result == "she finished 64th on race number 6 and he finished 42nd"

