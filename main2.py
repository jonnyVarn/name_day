#!/usr/bin/python3
import module1

m2 = module1.name()
my_dict = m2.answer_to_json_dict("skriv vad du vill default är ändå sholiday")
days_dict = m2.to_dict(my_dict)
Namnsdag = m2.get_namnsdag(days_dict)
Date = m2.get_date(days_dict)
m2.save_to_file(Namnsdag, Date)
