# Subject
"""
You need to modify the string of each data object to display
the following greetings:
"Hello World",
"Hello «country of your campus»",
"Hello «city of your campus»",
"Hello «name of your campus»"
"""

# initial variables
ft_list = ["Hello", "tata!"]
ft_tuple = ("Hello", "toto!")
ft_set = {"Hello", "tutu!"}
ft_dict = {"Hello": "titi!"}


# My code
ft_list[1] = "World!"

ft_tuple = "Hello", "France!"

ft_set.remove("tutu!")
ft_set.add("Paris!")
ft_set = sorted(ft_set)

ft_dict["Hello"] = "42Paris!"


# Results
print(ft_list)
print(ft_tuple)
print(ft_set)
print(ft_dict)
"""
Expected output:
$>python Hello.py | cat -e
['Hello', 'World!']$
('Hello', 'France!')$
{'Hello', 'Paris!'}$
{'Hello': '42Paris!'}$
"""
