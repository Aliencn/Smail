###Smail  
Python send mail  

###Installation  
Python 3.4 or later  

From pip
```
pip install Smail
```
###Use
```
from Smail import Smail  
a=Smail()  
a.set_server("smtp.exmail.qq.com",465,"admin@aliencn.net","password")  
a.set_subject('hello')  
a.set_content('world')  
a.add_to_addr('admin@aliencn.net')  

#Optional  
a.add_cc_addr('admin1@aliencn.net')  
a.add_cc_addr('admin2@aliencn.net')  
a.add_bcc_addr('admin3@aliencn.net')  
a.add_bcc_addr('admin4@aliencn.net')  
a.add_attachment(r'D:\Alien_System\Desktop\0.jpg')  
a.add_attachment(r'D:\Alien_System\Desktop\1.exe')  

#send mail now  
a.send()  
```