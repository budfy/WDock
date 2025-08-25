import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui.about_window import AboutWindow

def main():
    app = QApplication(sys.argv)
    
    # Create and show the about window
    about_window = AboutWindow()
    about_window.exec()
    
    sys.exit(0)

if __name__ == "__main__":
    main()