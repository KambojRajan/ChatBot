from customtkinter import *
import customtkinter as ct
from tkinter import *
from chat import getResponse,bot_name


ct.set_appearance_mode("dark")
ct.set_appearance_mode("dark-blue")

class ChatApp:
    def __init__(self) :
        self.window = CTk()     # this is the main screen it will act like the 
                                # container for any other label and it is the
                                # master of everyone
        self.UserMsgHeaight = 0.02
        self.ArsaMsgHeaight = 0.11
        self.ArsaChat = []
        self.UserChat = []
        self.WindowSetUp()

    def chaters(self):   
        # ArsaImage = CTkImage()

        self.textByUser = CTkTextbox(self.window,width=10,height=1,bg_color="white",fg_color="#bef8e4")
        self.textByUser.place(relheight = 0.75,relwidth = 0.5,rely = 0.07,relx = 0)
        self.textByUser.configure(cursor="arrow",state=DISABLED)
        scrollbar = CTkScrollbar(self.textByUser)
        scrollbar.place(relheight = 1,relx = 0.974)
        scrollbar.configure(command = self.textByUser.yview)


        self.textByArsa = CTkTextbox(self.window,width=10,height=1,bg_color="white",fg_color="#bef8e4")
        self.textByArsa.place(relheight = 0.75,relwidth = 0.5,rely = 0.07,relx = 0.5)
        self.textByArsa.configure(cursor="arrow",state=DISABLED)
        scrollbar = CTkScrollbar(self.textByArsa)
        scrollbar.place(relheight = 1,relx = 0.974)
        scrollbar.configure(command = self.textByArsa.yview)

    def run(self):
        self.window.mainloop()

    def optionmenu_callback(choice):
        print("")

    def options(self):
            option = StringVar()
            option.set("dark")
            dropDown = CTkOptionMenu(self.window,option = ["dark","light","system"])
            dropDown.place(relwidth = .25,relx = .75)

    def WindowSetUp(self):
        #seting the window and the dimenssions of its
        self.window.title("Chat")
        self.window.resizable(width = True,height= True)
        self.window.configure(width = 500,height=700,bg_color = "#026161")
        # seting a welcome label on the top 
        headLabel = CTkLabel(master=self.window,bg_color="darkblue",fg_color="#026161",text_color="ivory",text = "Arsa",pady = 10)
        headLabel.place(relwidth = 1)


    





        # seting two column for the text of User and Arsa
        ChatApp.chaters(self)

        bottonLabel = CTkLabel(self.window,bg_color="white",height=80)
        bottonLabel.place(relwidth = 1,rely = 0.825)

        self.inputSpan = CTkEntry(bottonLabel,fg_color="olive")
        self.inputSpan.place(relwidth = .77,relheight = 1)
        self.inputSpan.focus()
        self.inputSpan.bind("<Return>",self.onClick)
        send = CTkButton(bottonLabel,text = "Send",width=20,bg_color="#2a3636",fg_color="#2a3636",command=lambda:self.onClick(NONE))
        send.place(relx = 0.77,rely = 0.008,relheight = 1,relwidth = 0.22)


    def onClick(self,event):
        msg = self.inputSpan.get()
        self.inputMsg(msg,"you")
    
    def inputMsg(self,msg,sender):
        
        if not msg:
            return
        self.inputSpan.delete(0,END)
        
        self.UserInput = CTkTextbox(self.textByUser,width=20,height=50,text_color="black",fg_color="darkcyan")
        self.ArsaInput = CTkTextbox(self.textByArsa,width=20,height=50,text_color="white",fg_color="darkseagreen")
        msg1 = f"{sender} : {msg}\n\n"
        self.UserInput.insert(END,msg1)
        self.textByUser.configure(state = NORMAL)
        self.UserInput.place(relwidth = .97,relheight = 0.13,rely = self.UserMsgHeaight)
        self.textByUser.configure(state = DISABLED)
        
        msg2 = f"{bot_name} : {getResponse(msg)}\n\n"
        self.ArsaInput.insert(END,msg2)
        self.textByArsa.configure(state = NORMAL)
        self.ArsaInput.place(relwidth = .97,relheight = 0.13,rely = self.ArsaMsgHeaight)
        self.textByArsa.configure(state = DISABLED) 
        self.ArsaChat.append(id(self.ArsaInput))
        self.UserChat.append(id(self.UserInput))
        # print(len(self.ArsaChat)," ",len(self.UserChat))
        self.UserMsgHeaight += 0.19   
        self.ArsaMsgHeaight += 0.19   
        if (len(self.ArsaChat) + len(self.UserChat))%10 == 0: 
            self.UserMsgHeaight = 0.02
            self.ArsaMsgHeaight = 0.11

    



if __name__ == "__main__":
    app = ChatApp()
    app.run()













