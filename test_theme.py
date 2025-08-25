import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from src.ui.about_window import AboutWindow

def main():
    app = QApplication(sys.argv)
    
    # Create a simple test window
    window = QWidget()
    window.setWindowTitle("Theme Test")
    layout = QVBoxLayout()
    
    # Add a button to show the about window
    button = QPushButton("Show About Window")
    about_window = AboutWindow(window)
    button.clicked.connect(about_window.exec)
    layout.addWidget(button)
    
    # Add a label to show current theme
    theme_label = QLabel()
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        theme = "Light" if value == 1 else "Dark"
    except:
        theme = "Unknown"
    
    theme_label.setText(f"System Theme: {theme}")
    layout.addWidget(theme_label)
    
    window.setLayout(layout)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()