# ASL-to-Text
# Ubiquitous Computing final project, Spring 2016
# Authors: Kevin Dibble, Jasmine Moran, Susan Souza
# File description:
#   This is the main file of the project. This acts as the entry point to the
#   "meat and potatoes" of the project. It additionally contains project information
#   like version and status.
#

__author__ = "Kevin Dibble, Jasmine Moran, Susan Souza"
__version__ = "0.9"
__status__  = "Development"

import gui

#main holder for the entry point to the project
def main():
   gui.go()

#start the project
if __name__ == '__main__':
   print("let's go!")
   main()
