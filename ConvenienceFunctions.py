# These functions are from stack overflow
from datetime import datetime, timedelta

def is_not_integer_or_zero(x):
    if x.isdigit() and int(x) > 0:
        return False
    else:
        print('Please enter a positive integer greater than 0.')
        return True

def is_not_integer(x):
    if x.isdigit():
        return False
    else:
        print('Please enter a positive integer.')
        return True

def is_not_one_or_two(x):
    try:
        x = int(x)
        if x == 1 or x == 2:
            return False
        else:
            return True
    except:
        print('Please enter 1 or 2.')
        return True


def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


#gets start and end of a week given some date
def week_magic(day):
    dt = datetime.strptime(day, '%Y-%m-%d')
    start = dt - timedelta(days=(dt.weekday()+1))
    end = start + timedelta(days=6)
    start = start.date()
    end = end.date()
    return start, end
