import requests as RQ
import json
from subprocess import Popen as Popen
from subprocess import check_output as check_output
from time import sleep


class name:

    def __init__(self):
        my_url = "https://sholiday.faboul.se/dagar/v2.1/"
        self.my_url = my_url

    def answer_to_json_dict(self, my_url):
        # had to do this in one step.
        # defaults to faboul for convinience
        my_url = self.my_url
        fabol_answer = RQ.api.get(my_url)
        my_dict = fabol_answer.json()
        return my_dict

    def to_dict(self, my_dict):
        # because this is a nested flat dict thingy
        days = my_dict['dagar']
        days_dict = days[0]
        return days_dict

    def get_namnsdag(self, days_dict):
        #haha got my namnsdag
        names = days_dict.get('namnsdag')
        return names

    def get_date(self, days_dict):
        #took the date to perhaps i will need it
        date = days_dict.get('datum')
        return date
    
    def systemctl_reload(self):
        #this was kind of boring to do lots of times when I change in unit-files
        Popen(["systemctl" ,"daemon-reload"])

    def save_to_file(self, name_day, date):
        
        try:
            #well not much to say try to open names 
            file_test=open('names.txt')
            test=str(file_test.readlines)
            print(test)
            #if the names.txt does not contain the current date
            if not test.find(date)==-1:
                file = open('names.txt', 'a+') #open in append+ mode..
                file.write(date + " Dagens namn: ")  #write date and namsdag..
                #this is just to end with a . or , nothing more..
                for i in range(len(name_day)):   
                    if i != len(name_day)-1:
                        file.write(name_day[i] + ", ")
                    else:
                        file.write(name_day[i] + ".")
                        file.write("\n")
                print("done writing to file")
            else:
                print("did not write will sleep for a while")
                sleep(60) #could have used more but..this is nothing usefull anyway
        except:
            #well the file is not there yet so no risk in writing the name again..
            print("the file is not ready yet so I guess its ok")
            file = open('names.txt', 'a+')
            file.write(date + " Dagens namn: ")
            for i in range(len(name_day)):
                if i != len(name_day)-1:
                    file.write(name_day[i] + ", ")
                else:
                    file.write(name_day[i] + ".")
            file.write("\n")
            print("done writing to file")
            
        #this kind of creates a init script have not tested..
    def create_init_script(self):
        file = open('namnsdag.sh', 'w+')
        file.write("#!/usr/bin/bash \n"
                   "### BEGIN INIT INFO + \n"
                   "# Provides:          namnsdag service \n"
                   "# Required-Start: \n"
                   "# Required-Stop:     $local_fs \n"
                   "# Default-Start:     2 3 4 5 \n"
                   "# Default-Stop:      0 1 6 \n"
                   "# Short-Description: namnsdag service \n"
                   "# Description:       namnsdag service \n"
                   "### END INIT INFO\t")
        file.close()
        Popen(["sudo", "chmod", "+x", "namnsdag.sh"])
        Popen(["cp", "time.sh", "/etc/init.d/namnsdag.sh"])
        Popen(["chmod", "+x", "/etc/init.d/namnsdag.sh"])

        #this creates the sh file..
    def create_namnsdag_sh(self):
        #this should use the "main2.py"
        # creates a sh file and stuff
        pwd_binary = check_output(["pwd"], shell=True)
        pwd = pwd_binary.decode()
        pwd_str = pwd.strip("\n")
        print(pwd)
        whole_pwd = pwd_str + "/main2.py"
        bash_str = "#!/bin/bash"
        file99 = open('namnsdag.sh', 'w+')
        file99.write(f"{bash_str} \n  {whole_pwd}")
        file99.close()
        Popen(["sudo", "chmod", "+x", "main2.py"])

        #this copies.. 
    def copy_namnsdag_sh(self): 
        Popen(["sudo", "chmod", "+x", "namnsdag.sh"])
        Popen(["cp", "namnsdag.sh", "/usr/bin/namnsdag.sh"])
        Popen(["sudo", "chmod", "+x", "/usr/bin/namnsdag.sh"])
    
        #this create a unit-file.. fun
    def create_namnsdag_service(self):
        file1 = open('namnsdag.service', 'w+')
        file1.write("[Unit]\n"
                    "Description=Namnsdag Service \n"
                    "After=network.target \n"
                    "StartLimitIntervalSec=0\n"
                    "[Service] \n"
                    "Type=simple \n"
                    "Restart=always\n"
                    "RestartSec=1\n"
                    "User=root \n"
                    "ExecStartPre= \n"
                    "ExecStart=/usr/bin/namnsdag.sh \n"
                    "ExecStartPost= \n"
                    "ExecStop= \n"
                    "ExecReload= \n"
                    "[Install] \n"
                    "WantedBy=multi-user.target \t")
        file1.close()
        Popen(["cp", "namnsdag.service", "/etc/systemd/system/namnsdag.service"])

        Popen(["systemctl", "start", "namnsdag.service"])


"""logg days before played with https://github.com/jonnyVarn/time and had christmas leave. 
2020-12-26 started with this assignment perhaps I should have done this before,
but It was hard to descide but here it is. https://github.com/jonnyVarn/name_day/
almost sort of working sleeps one hour if finds the current date.

2020-12-27 created repo from github webpage
2020-12-27 created and added  __init__.py git add __init__.py git commit -m "added __init__.py" git push
2020-12-27 added file namesday.py 
2020-12-27 needed a systemd linux run old ubuntu mate on laptop and messed around
2020-12-27 had problems with importing so renamed to module1.py and function to skapa have not pushed yet.
2020-12-27 cloning from another computer..
2020-12-27 rewrote as oob still no git push trying to fix first..
dec 28 00:39:21 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:2: Assignment outside of section. Ignoring.
dec 28 00:39:21 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:3: Assignment outside of section. Ignoring.
dec 28 00:39:21 josefs-MacBookPro systemd[1]: namnsdag.service: Service lacks both ExecStart= and ExecStop= setting. Refusing.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:2: Assignment outside of section. Ignoring.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:3: Assignment outside of section. Ignoring.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: namnsdag.service: Service lacks both ExecStart= and ExecStop= setting. Refusing.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:2: Missing '='.
cat /etc/systemd/system/namnsdag.service
#!/usr/bin/bash
/home/jw/name
"python3 __main__.py
hm ;) not intended..
line 95 ;) Popen(["cp", "namnsdag.sh", "/etc/systemd/system/namnsdag.service"])
ok.. so
cat /etc/systemd/system/namnsdag.service
[Unit]
Description=Namnsdag Service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStartPre=
ExecStart=/usr/bin/namnsdag.sh
ExecStartPost
ExecStop=
ExecReload=
[Install]
WantedBy=multi-user.target
looks better but still
 namnsdag.service
   Loaded: error (Reason: Invalid argument)
   Active: inactive (dead)

dec 28 00:39:21 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:2: Assignment outside of section. Ignoring.
dec 28 00:39:21 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:3: Assignment outside of section. Ignoring.
dec 28 00:39:21 josefs-MacBookPro systemd[1]: namnsdag.service: Service lacks both ExecStart= and ExecStop= setting. Refusing.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:2: Assignment outside of section. Ignoring.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:3: Assignment outside of section. Ignoring.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: namnsdag.service: Service lacks both ExecStart= and ExecStop= setting. Refusing.
dec 28 00:39:58 josefs-MacBookPro systemd[1]: /etc/systemd/system/namnsdag.service:2: Missing '='.
so i guess i have to restart service
sudo systemctl daemon-reload
rm namnsdag.service då..
sudo systemctl daemon-reload igen..
missed a = 

looks better but still no go
and i should have added a bit off sleep to the program and me ;)

systemctl status namnsdag.service
● namnsdag.service - Namnsdag Service
   Loaded: loaded (/etc/systemd/system/namnsdag.service; disabled; vendor preset: enabled)
   Active: activating (auto-restart) (Result: exit-code) since Mon 2020-12-28 00:58:31 CET; 732ms ago
  Process: 20647 ExecStart=/usr/bin/namnsdag.sh (code=exited, status=203/EXEC)
 Main PID: 20647 (code=exited, status=203/EXEC)

journalctl -xe gives me a clue..
 The start-up result is RESULT.
dec 28 01:00:55 josefs-MacBookPro systemd[20985]: namnsdag.service: Failed to execute command: No such file or directory
dec 28 01:00:55 josefs-MacBookPro systemd[20985]: namnsdag.service: Failed at step EXEC spawning /usr/bin/namnsdag.sh: No such file or directory
hm.. didnt  copy.. the file there ?
ls /usr/bin/namnsdag.sh
/usr/bin/namnsdag.sh and its green and pretty..
/usr/bin/namnsdag.sh
-bash: /usr/bin/namnsdag.sh: /usr/bin/bash: felaktig tolk: Filen eller katalogen finns inte
hm hm.. cat perhaps..
cat /usr/bin/namnsdag.sh
#!/usr/bin/bash
/home/jw/name
"python3 __main__.py
not as it should..
still not working but doing some git anyway..
git config --global user.email "darth.vader@rymdimperiet.nu"
jw@josefs-MacBookPro:~/name_day$ git add __main__.py
jw@josefs-MacBookPro:~/name_day$ git commit -m "changed a bit"
[main 4f645f0] changed a bit
 2 files changed, 203 insertions(+)
 mode change 100644 => 100755 __main__.py
 create mode 100644 module1.py
  git rm namesday.py
git commit -m "removed namesday.py"
[main 16ae616] removed namesday.py
 1 file changed, 65 deletions(-)
 delete mode 100644 namesday.py
 git push
Username for 'https://github.com': jonnyvarn
Password for 'https://jonnyvarn@github.com':
Räknar objekt: 2, klart.
Delta compression using up to 4 threads.
Komprimerar objekt: 100% (2/2), klart.
Skriver objekt: 100% (2/2), 225 bytes | 225.00 KiB/s, klart.
Total 2 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/jonnyVarn/name_day
   4f645f0..16ae616  main -> main
   perhaps i missed some stuff..

my mind goes in cirkles and so does my code..
namnsdag.service - Namnsdag Service
   Loaded: loaded (/etc/systemd/system/namnsdag.service; disabled; vendor preset: enabled)
   Active: activating (auto-restart) since Mon 2020-12-28 05:57:34 CET; 494ms ago
  Process: 31070 ExecStart=/usr/bin/namnsdag.sh (code=exited, status=0/SUCCESS)
 Main PID: 31070 (code=exited, status=0/SUCCESS)
 added main2 because i created and edited the same files ;) I'm to tired.
 It will be a fun day today.
 


"""
