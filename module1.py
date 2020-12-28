import requests as RQ
import json
from subprocess import Popen as Popen
from subprocess import check_output as check_output



class name:
    
    def __init__(self):
        my_url = "https://sholiday.faboul.se/dagar/v2.1/"
        self.my_url = my_url

    
    def answer_to_json_dict(self, my_url):
        #had to do this in one step.
        #defaults to faboul for convinience
        my_url=self.my_url
        fabol_answer=RQ.api.get(my_url)
        my_dict=fabol_answer.json()
        return my_dict

    def to_dict(self, my_dict):
        #because this is a nested flat dict thingy
        days=my_dict['dagar']
        days_dict=days[0]
        return days_dict

    def get_namnsdag(self, days_dict): 
        names=days_dict.get('namnsdag')
        return names
    
    def get_date(self, days_dict):   
        date=days_dict.get('datum')
        return date
    
    def save_to_file(self, name_day, date):
        file=open('names.txt', 'a+')
        file.write(date +" Dagens namn: ")
        for i in range(len(name_day)):
            if i!=len(name_day)-1:
                file.write(name_day[i] + ", ")
        else:
            file.write(name_day[i] +".")
        file.write("\n")
        print("done writing to file")

    def create_init_script(self):
        file=open('namnsdag.sh', 'w+')
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
        Popen(["sudo","chmod", "+x", "namnsdag.sh"])
        Popen(["cp", "time.sh", "/etc/init.d/namnsdag.sh"])
        Popen(["chmod", "+x", "/etc/init.d/namnsdag.sh"])

    def create_systemd_service(self):
        #creates a sh file and stuff
        pwd_binary = check_output(["pwd"], shell=True)
        pwd=pwd_binary.decode()
        print(pwd)
        whole_pwd=pwd+"/__main__.py"
        print(whole_pwd)
        file=open('namnsdag.sh', 'w+')
        file.write("#!/usr/bin/bash " +"\n" +whole_pwd)
        file.close()
        Popen(["sudo","chmod", "+x", "namnsdag.sh"])
        Popen(["cp", "namnsdag.sh", "/usr/bin/namnsdag.sh"])
        Popen(["sudo","chmod", "+x", "/usr/bin/namnsdag.sh"])
        file1=open('namnsdag.service', 'w+')
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
       
        

        Popen(["systemctl", "start" ,"namnsdag.service"])


"""logg

https://github.com/jonnyVarn/name_day/
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


"""