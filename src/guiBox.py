from Tkinter import *
import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]

import Leap
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

### begin MVC GUI implementation ###

class Ctrl:
   def __init__(self, root):
      self.root = root
      self.view = View(root)
      self.model = Model(self)
      self.view.setSubtitle("ASL to Text")
      listener = aslListener()
      controller = Leap.Controller()
      controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
      controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
      controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
      controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

      listener.extraUtils(self.model) #ensure the listener can send changes to the model

      controller.add_listener(listener)
      self.root.mainloop()
      print "Press Enter to quit..."
      #need to replace this block with some input from View to trigger exit and so on
      try:
         sys.stdin.readline()
      except KeyboardInterrupt:
         pass
      finally:
      # Remove the sample listener when done
         controller.remove_listener(listener)
   #do thing when model updated

   def gotTxtUpdate(self):
      self.view.setSubtitle(self.model.getText())
      #print "ctrl got: " + self.model.getText()

class Model():

   def __init__(self, ctrl):
      self.ctrl = ctrl
      self.txt = "ASL to Text"

   def getText(self):
      return self.txt

   def textChanged(self, text):
      if len(self.txt) < 12:
         self.txt = self.txt + text
      else:
         self.txt = text
      self.ctrl.gotTxtUpdate()  #signal controller of change

class View:
   def loadView(self):
      self.subtitle = Label(self.ctrl, font=('Helvetica','36'), fg='gray23', bg='gray30', anchor=S, pady=50)
      self.subtitle.master.wm_attributes("-topmost", True)
      self.subtitle.master.wm_attributes("-transparentcolor", "gray30")
      self.subtitle.pack(fill=BOTH, expand=1, side=BOTTOM)

   def __init__(self, ctrl):
     self.ctrl = ctrl
     self.loadView()

   def setSubtitle(self, txt):
      self.subtitle.configure(text = txt)
      #print "model updating"

### end MVC GUI implementation ###
#
COMPARISON_PERCENT = 50

def get_angles(vector_array):
   return_array = []
   i = 0
   while (i < 5):
      j = 0
      while (j < 5):
         return_array.append(vector_array[i].angle_to(vector_array[j]))
         j = j + 1
      i = i + 1
   return return_array

def compare(base_letter, compare_letter):
   # loop through each finger and compare the two letters together
   i = 0
   all_match = True
   while (i < 5):
    #   print "\ni = %d" % (i)
      j = 0
      while (j < 5):
        #  print "\tj = %d" % (j)
        # compare this i/j pairing
        #  print "%s and %s" % (base_letter[i], base_letter[j])
         base_dot = base_letter[i].angle_to(base_letter[j])
         compare_dot = compare_letter[i].angle_to(compare_letter[j])
        #  print ""
         print "%s and %s" % (base_dot, compare_dot)
         if (base_dot < 0.001 and base_dot > -0.001):
            comparison = 0
         else:
            comparison = 100 * (compare_dot - base_dot) / base_dot
         #print "percentage comparison %s" % (comparison)
         if comparison < COMPARISON_PERCENT and comparison > (COMPARISON_PERCENT * -1):
            all_match = all_match and True
         else:
            all_match = False
         j = j + 1
      i = i + 1
      print ""
   print "all_match: %s\n" % (all_match)
   return all_match

def compare_angles_thumb(base_angles, compare_vectors):
   all_match = True
   compare_angles = get_angles(compare_vectors)
   i = 0
   while (i < 5):
    #   print "%s and %s" % (base_angles[i], compare_angles[i])
      comparison = 100 * (compare_angles[i] - base_angles[i]) / (base_angles[i] + 0.00000001)
      #print "percentage comparison %s" % (comparison)
      if abs(comparison) < COMPARISON_PERCENT:
         all_match = all_match and True
      else:
         all_match = False
      i = i + 1

   print "all_match: %s\n" % (all_match)
   return all_match

def compare_angles(base_angles, compare_vectors):
   all_match = True
   compare_angles = get_angles(compare_vectors)
   i = 0
   while (i < len(base_angles)):
    #   print "%s and %s" % (base_angles[i], compare_angles[i])
      comparison = 100 * (compare_angles[i] - base_angles[i]) / (base_angles[i] + 0.00000001)
      #print "percentage comparison %s" % (comparison)
      if comparison < COMPARISON_PERCENT and comparison > (COMPARISON_PERCENT * -1):
         all_match = all_match and True
      else:
         all_match = False
      i = i + 1

   #print "all_match: %s\n" % (all_match)
   return all_match

#a subclass of Leap.Listener based on Sample.py
class aslListener(Leap.Listener):
   finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
   #prev_letter = "B"
   #allows the listener to communicate with the model
   #listener instantiated in Ctrl
   def extraUtils(self, model):
      self.report = model

   def on_init(self, controller):
      print "Initialized"

   def on_connect(self, controller):
      print "Connected"

   def on_disconnect(self, controller):
      print "Disconnected"

   def on_exit(self, controller):
      print "Exited"

   def on_frame(self, controller):
    #  finger_vectors = [Leap.Vector(0.260498, -0.677901, 0.687452),
    #     Leap.Vector(-0.393398, 0.827915, -0.399743),
    #     Leap.Vector(-0.39042, 0.813348, -0.431321),
    #     Leap.Vector(-0.286566, 0.8197, -0.495956),
    #     Leap.Vector(-0.216815, 0.854775, -0.47154)]

    #letter_angles = [thumb and thumb,
    #   thumb and index,
    #   thumb and middle,
    #   thumb and ring,
    #   thumb and pinkly,
    #   index and thumb,
    #   index and index,
    #   index and middle,
    #   index and ring,
    #   index and pinky,
    #   middle and thumb,
    #   middle and index,
    #   middle and middle,
    #   middle and ring,
    #   middle and pinky,
    #   ring and thumb,
    #   ring and index,
    #   ring and middle,
    #   ring and ring,
    #   ring and pinky,
    #   pinky and thumb,
    #   pinky and index,
    #   pinky and middle,
    #   pinky and ring,
    #   pinky and pinky]

      A_angles = [0.0,
          2.8812789917,
          2.859770298,
          2.84813141823,
          2.73459911346,
          2.8812789917,
          0.0,
          0.118831209838,
          0.228779360652,
          0.383088201284,
          2.859770298,
          0.118831209838,
          0.0,
          0.117045581341,
          0.267506659031,
          2.84813141823,
          0.228779360652,
          0.117045581341,
          0.0,
          0.154956310987,
          2.73459911346,
          0.383088201284,
          0.267506659031,
          0.154956310987,
          0.0]
      B_angles =[0.0,
           0.439740777016,
           0.527846693993,
           0.577073693275,
           0.63708627224,
           0.439740777016,
           0.0,
           0.100545287132,
           0.154377490282,
           0.201784655452,
           0.527846693993,
           0.100545287132,
           0.0,
           0.0538404807448,
           0.109854474664,
           0.577073693275,
           0.154377490282,
           0.0538404807448,
           0.0,
           0.0698691532016,
           0.63708627224,
           0.201784655452,
           0.109854474664,
           0.0698691532016,
           0.0]
      C_angles = [0.0,
         0.565682411194,
         0.548766136169,
         0.647555172443,
         1.09946036339,
         0.565682411194,
         0.0,
         0.0179408397526,
         0.352951109409,
         0.841872930527,
         0.548766136169,
         0.0179408397526,
         0.0,
         0.346947342157,
         0.840921521187,
         0.647555172443,
         0.352951109409,
         0.346947342157,
         0.0,
         0.51339751482,
         1.09946036339,
         0.841872930527,
         0.840921521187,
         0.51339751482,
         0.51339751482]
      D_angles = [0.0,
           0.880243360996,
           1.00771903992,
           1.9491314888,
           2.23631477356,
           0.880243360996,
           0.0,
           0.395872354507,
           2.08581185341,
           2.18799972534,
           1.00771903992,
           0.395872354507,
           0.0,
           1.69160568714,
           1.80022823811,
           1.9491314888,
           2.08581185341,
           1.69160568714,
           0.0,
           0.291275531054,
           2.23631477356,
           2.18799972534,
           1.80022823811,
           0.291275531054,
           0.291275531054]
      E_angles = [ 0.0,
         0.308618754148,
         2.73403167725,
         2.82854390144,
         2.84681677818,
         0.308618754148,
         0.0,
         3.0257191658,
         3.04934453964,
         2.96922564507,
         2.73403167725,
         3.0257191658,
         0.0,
         0.104628279805,
         0.17910091579,
         2.82854390144,
         3.04934453964,
         0.104628279805,
         0.0,
         0.0865492895246,
         2.84681677818,
         2.96922564507,
         0.17910091579,
         0.0865492895246,
         0.0865492895246]
      F_angles = [ 0.0,
         1.96462583542,
         0.490814357996,
         0.490148037672,
         0.459969967604,
         1.96462583542,
         0.0,
         2.21380853653,
         2.40438628197,
         2.42444562912,
         0.490814357996,
         2.21380853653,
         0.0,
         0.249927476048,
         0.422325372696,
         0.490148037672,
         2.40438628197,
         0.249927476048,
         0.0,
         0.190423130989,
         0.459969967604,
         2.42444562912,
         0.422325372696,
         0.190423130989,
         0.190423130989]
      G_angles = [0.0,
         1.06423842907,
         0.987863242626,
         1.54763281345,
         2.09381890297,
         1.06423842907,
         0.0,
         0.189559593797,
         1.38221013546,
         1.9089962244,
         0.987863242626,
         0.189559593797,
         0.0,
         1.22131979465,
         1.78623831272,
         1.54763281345,
         1.38221013546,
         1.22131979465,
         0.0,
         0.626338541508,
         2.09381890297,
         1.9089962244,
         1.78623831272,
         0.626338541508,
         0.626338541508]
      all_letter_angles = [A_angles, B_angles, C_angles, D_angles, E_angles, F_angles, G_angles]
      letter_names = [
         "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
         "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
      frame = controller.frame()
      #print "got a frame"

      for hand in frame.hands:
         handType = "Left hand" if hand.is_left else "Right hand"
        #  print "%s" % (hand.pointables[1].direction)
         # Get fingers
         #for finger in hand.fingers:
            #print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
            #   self.finger_names[finger.type],
            #   finger.id,
            #   finger.length,
            #   finger.width)
         #print "\n"

        #  for finger in hand.fingers:
        #     distal_direction = finger.bone(3).direction
        #     print "direction %s" % (distal_direction)
         current_vectors = []
         for finger in hand.fingers:
            current_vectors.append(finger.bone(3).direction)
            # print "%s" % (finger.bone(3).direction)
         letter_index = 0
         all_match = False
         for letter in all_letter_angles:
            all_match = compare_angles_thumb(letter, current_vectors)
            if all_match:
               break
            letter_index = letter_index + 1
        #  all_match = compare(finger_vectors, current_vectors)
        #  all_match = compare(finger_vectors, hand.pointables)
        #  for pointable in hand.pointables:
        #      #print " direction %s" % (pointable.direction)
        #      dot_product = pointable.direction.dot(finger_vectors[i])
        #      #print "dot product %s" % (dot_product)
        #      if dot_product > 0.94:
        #         all_match = all_match and True
        #      else:
        #         all_match = False
        #      #print "%s all_match" % (all_match)
        #      i = i + 1
         if all_match:
            print "match %s!" % (letter_names[letter_index])
            self.report.textChanged(letter_names[letter_index])
            #self.prev_letter = letter_names[letter_index]

         print "\n\n"
         time.sleep(.5)

    #   for gesture in frame.gestures():
    #
    #      if gesture.type is Leap.Gesture.TYPE_CIRCLE:
    #         #print "circle"
    #         self.report.textChanged("circle")
    #      elif gesture.type is Leap.Gesture.TYPE_SWIPE:
    #         #print "swipe"
    #         self.report.textChanged("swipe")
    #      elif gesture.type is Leap.Gesture.TYPE_KEY_TAP:
    #         #print "key tap"
    #         self.report.textChanged("key tap")
    #      elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
    #         #print "screen tap"
    #         self.report.textChanged("screen tap")


def main():
   root = Tk()
   root.title('ASL-to-Text')
   root.attributes("-fullscreen", True) #for fullscreen
   app = Ctrl(root)


if __name__ == '__main__':
    main()

#refs:
#  Leap:
#     https://developer.leapmotion.com/documentation/python/api/Leap.Gesture.html#Leap.Gesture.html
#     https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
#  Tkinter & MVC:
#     https://tkinter.unpythonic.net/wiki/ToyMVC
#     http://ygchan.blogspot.com/2012/05/python-stop-watch-timer-source-code.html
#     http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png
