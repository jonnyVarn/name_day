#!/usr/bin/python3
import module1

m1 = module1.name()
my_dict=m1.answer_to_json_dict("skriv vad du vill default är ändå sholiday")
days_dict=m1.to_dict(my_dict)
Namnsdag=m1.get_namnsdag(days_dict)
Date=m1.get_date(days_dict)
m1.save_to_file(Namnsdag, Date)
m1.create_systemd_service()




