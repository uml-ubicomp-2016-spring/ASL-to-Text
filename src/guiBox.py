from Tkinter import *



class GuiCtrl:
   def __init__(self, root):
      self.model = ModelReporter(self)
      self.root = root
      self.view = View(self.root)
      self.view.setSubtitle('')
   #do thing when model updated
   
   def gotTxtUpdate(self):
      self.view.setSubtitle(self.modelReporter.getText())

      
      
class View:
   def loadView(self):
      self.subtitle = Label(self.ctrl, font=('Helvetica','36'), text = "TEST", fg='black', bg='gray30', wraplength=80, anchor=S, pady=50) #for fullscreen
      self.subtitle.master.wm_attributes("-topmost", True)
      self.subtitle.master.wm_attributes("-transparentcolor", "gray30")
      self.subtitle.pack(fill=BOTH, expand=1, side=BOTTOM)

   def __init__(self, ctrl):
     self.ctrl = ctrl.root
     self.loadView()

     
   def setSubtitle(self, txt):
      self.subtitle.configure(text = txt)
     
   
class ModelReporter():
   
   def __init__(self, ctrl):
      self.ctrl = ctrl
      self.txt = "TEST"
      
   
   def getText(self):
      return self.txt
   
   def textChanged(self, text):
      if 160 < len(self.txt):
         self.txt = ""
      self.txt = self.txt + text
      self.ctrl.gotTxtUpdate()  #signal controller of change
     
     
def main():
   root = Tk()
   root.title('GUI Box Test')
   root.attributes("-fullscreen", True) #for fullscreen
   app = GuiCtrl(root)
   root.mainloop()    
 
if __name__ == '__main__':
    main()  