def sleep_decorator(function):


    def wrapper(num):
        print num
        return function(num)
    return wrapper


@sleep_decorator
def print_number(num):
    return num

print(print_number(222))
