try:
    import Tkinter as tk
except:
    import tkinter as tk
from twilio.rest import Client
from gpiozero import LED
import time
import threading
from twilio.rest import Client


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("400x250")
        self.create_widgets() 
        self.relay = LED(23)
        self.relay.on()
    
    def create_widgets(self):
        self.OptionList = ['10', '15','25', '30', '45', '60']
        self.sms_dict = {'YOUR_NAME':'YOUR_PHONE_NUMBER', 'No SMS': None, }
        self.start_button = tk.Button(self, text ="Start", command = self.start, height = 2, width = 10, fg='black') 
        self.start_button.place(x=250, y=200)

        self.stop_button = tk.Button(self, text ="Stop", command = self.stop, height = 2, width = 10, fg='black') 
        self.stop_button.place(x=50, y=200)

        self.variable = tk.StringVar()
        self.variable.set(self.OptionList[3])
        self.last_value = int(self.variable.get())
        self.time_menu = tk.OptionMenu(self, self.variable, *self.OptionList)
        self.time_menu.place(x=80, y=50)
        self.variable.trace("w", self.callback)

        self.time_menu_label = tk.Label(self, font='TimesNewRoman 14', text="Time (min):")
        self.time_menu_label.place(x=65, y=20)

        self.variable_sms = tk.StringVar()
        self.variable_sms.set(list(self.sms_dict)[0])
        self.last_value_sms = str(self.variable_sms.get())
        
        self.sms_menu = tk.OptionMenu(self, self.variable_sms, *self.sms_dict)
        self.sms_menu.place(x=265, y=50)
        self.variable_sms.trace("w", self.sms_callback)

        self.sms_menu_label = tk.Label(self, font='TimesNewRoman 14', text="SMS notification to:")
        self.sms_menu_label.place(x=230, y=20)

        self.remaining_time_display = tk.Text(self, wrap='word', font='TimesNewRoman 34',bg=self.cget('bg'), relief='flat', width=10, height=1)
        self.remaining_time_display.place(x=140, y=100)
        
        
    
    def callback(self, *args):
        self.last_value = int(self.variable.get())

    def sms_callback(self, *args):
        self.last_value_sms = str(self.variable_sms.get())
        
        

    def start(self):
        self.status = False
        self.t1 = threading.Thread(target=self.time_counter, name='t1') 
        self.relay.off()
        self.t1.start()
        p.start()
        time.sleep(1)
        p.stop()
        

    def time_counter(self):
        self.seconds = 0
        self.sms_status = 0
        self.minutes = 0
        while (self.minutes <= self.last_value):

            self.remaining_minutes = self.last_value - self.minutes
            self.remaining_time_display.insert('end', str(self.remaining_minutes) + " min left")
            while (self.seconds <= 60 and self.sms_status != 1):
                time.sleep(1)
                self.seconds += 1
                if self.status == True:
                    self.sms_status = 1
                    self.relay.on()
                    break 
            self.remaining_time_display.delete(1.0, 'end') 
            self.minutes += 1

        self.finished()
    
    def finished(self):
        self.relay.on()
        if self.sms_status == 0 and  self.last_value_sms != 'No SMS':
            self.send_sms(sms_body='UV Neutralizer has completed its time. Your items are ready', to_number=self.sms_dict[self.last_value_sms])
        elif self.sms_status == 1 and self.last_value_sms != 'No SMS':
            self.send_sms(sms_body='UV Neutralizer has been stopped', to_number=self.sms_dict[self.last_value_sms])
            
        p.start()
        time.sleep(0.5)
        p.stop()
        time.sleep(0.5)
        p.start()
        time.sleep(0.5)
        p.stop()
        


    def send_sms(self, sms_body='', to_number=''):
        account_sid = 'YOUR TWILIO ACCOUNT SID'
        auth_token = 'YOUR TWILIO TOKEN'
        client = Client(account_sid, auth_token)
        client.messages.create(body=sms_body,from_='FROM YOUR TWILIO NUMBER',to=to_number)
    
    def stop(self):
        self.status = True
        print ('stopping')
        


application = Application()
application.title("UV Neutralizer | By Marco Mascorro")
application.mainloop()