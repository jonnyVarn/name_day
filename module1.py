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
                sleep(3600) #could have used more but..this is nothing usefull anyway
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
        Popen(["cp", "namnsdag.sh", "/etc/init.d/namnsdag.sh"])
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
 
 git add __main__.py module1.py main2.py
jw@josefs-MacBookPro:~/name_day$ git commit -m "added comments"
[main f830fd4] added comments
 1 file changed, 21 insertions(+), 10 deletions(-)
jw@josefs-MacBookPro:~/name_day$ git push
Username for 'https://github.com': jonnyvarn
Password for 'https://jonnyvarn@github.com':
To https://github.com/jonnyVarn/name_day
 ! [rejected]        main -> main (fetch first)
error: misslyckades sända vissa referenser till "https://github.com/jonnyVarn/name_day"
tips: Uppdateringar avvisades då fjärren innehåller ändringar som du inte
tips: har lokalt. Det beror oftast på att ett annat arkiv har sänt in samma
tips: referenser. Det kan vara en idé att först integrera fjärrändringarna
tips: (t.ex. "git pull ...") innan du sänder igen.
tips: Se avsnittet "Note about fast-forwards" i "git push --help" för detaljer.
jw@josefs-MacBookPro:~/name_day$ git push -f
Username for 'https://github.com': jonnyvarn
Password for 'https://jonnyvarn@github.com':
Räknar objekt: 32, klart.
Delta compression using up to 4 threads.
Komprimerar objekt: 100% (30/30), klart.
Skriver objekt: 100% (32/32), 7.77 KiB | 1.55 MiB/s, klart.
Total 32 (delta 12), reused 0 (delta 0)
remote: Resolving deltas: 100% (12/12), done.
To https://github.com/jonnyVarn/name_day
 + 7a1752b...f830fd4 main -> main (forced update)

copy paste från förra 
Jag använder mig av VIM med plugin airline, justify, matchit, powerline och python-jedi för att få en trevlig utvecklingsmiljö med autokomplettering och lite finare vim.                
Jag använder mig av VIM eftersom jag sitter på en Linux konsol via ssh.
Jag hade använt en annan terminalbaserad kanske emacs eftersom jag valt att inte köra grafiskt. Om jag hade kört grafiskt så hade jag antagligen kört visualstudiocode, pycharm, atom eller någon annan IDE.
Jag valde filhanterare eftersom den låg på först och verkade vara den mest användbara applikationen. 
Filhanteraren började växa och utvecklades till Linux-terminal-helper när jag tänkte att den skulle kunna vara lite stöd för andra när de jobbar i Linux/Unix möjligtvis finns det en  en framtid i windows i terminalmiljö.  
Linux är ju egentligen en Kärna Linux/GNU är ett operativsystem och det finns många olika varianter av GNU/Linux några av de största listas nedan.
RHEL eller RedhatEnterprise där även Linus Torvalds huserar med community drivna varianter som Centos.
Debian med varianter som Ubuntu som nästan har gått om Debian i antal användare.
Suse Enterprise Linux som från början startade i Tyskland ursprungligen från Slackware Linux.
Det alla Linux varianter delar är som sagt Linux kärnan.
I alla Linux varianter kan man installera .tgz paket eller så kallade tar bollar.
Enklast kan vara att dela upp Linux i vilken pakethanterare de använder för att lättare se släktskapet.
RHEL och Centos är i princip samma Os förutom enterprise supporten och de använder sig av pakhethanteraren yum som kom ifrån yellowdog-linux som var det enda linux som fungerade för mac powerpc på den tiden det begav sig. 
En lite mer krånglig variant är rpm RedhatPacketManager där man själv får hålla ordning på vilka dependencies som behövs.
Debian, ubuntu, ubuntu mate etc använder sig av pakethanteraren apt. Eller den lite krångligare varianten där man får använda sig av dependencies själv dpkg
i
Av de som står själva förtjänar Alpine linux att nämnas ett minimalt komplett Linux/GNU som från början var avsett att användas på accesspunkter och mindre inbyggda enheter.
Vad finns det för användningsområden inom Linux?
Användningsområden inom Linux är oändliga men för att ge några exempel kan man tala om olika typer av servrar exempelvis DHCP-server.
Det finns olika styrdatorer.
Jag skulle ju klassificera Android som en Linux kärna så telefoner är ju ett annat område där vi använder Linux.
Beskriv hur ni använt er av Linux i denna applikation
Jag har utvecklat min applikation på antix linux (ett debian derrivat med init istället för systemd)
Jag har använt Vim och kört den ifrån en Linux terminal, jag har även testat applikationen på ubuntu och en openbsd, vilket inte är linux.
Beskriv de olika tjänster ni känner till som finns i Linux
Ja eftersom en tjänst är ett program som körs i bakgrunden så blir ju svaret nästan oändligt.
Jag väljer att lista några av de vanligaste.
Brandväggar firewalld, ufw, ip-tables. Dessa är tjänster som kan kontrollera vilka TCP/UDP portar som är öppna in eller ut på Linux.
FTP File Transfer Protocol som erbjuder fildelning. Det finns såklart en uppsjö utav FTP varianter.
 Cron/cronnyd etc är en tjänst som startar tjänster efter tid.
 Cups erbjuder delning av skrivare och skrivartjänster.
 Ntp är NetworkTimeProtocol och erbjuder tidssynkronisering.
 Systemlog tjänster som loggar händelser på systemet. några exempel är syslog-ng och rsyslog.
 SSH secureShell bjuder möjlighet att logga in på en dator via TCP/IP och är ersättaren till det mindre säkrare Telnet. Det ju många olika varianter av ssh servrar men min favorit kommer från en av mina favorit operativsystem openbsd och heter openssh.
"""
