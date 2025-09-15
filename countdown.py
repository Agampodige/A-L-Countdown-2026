import sys
from PyQt6.QtCore import QTimer, Qt, QDateTime, QDate, QTime
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont

class CountdownOverlay(QWidget):
    def __init__(self, exam_date: QDate, display_number: int):
        super().__init__()
        
        # Set the exam date and target display
        self.exam_datetime = QDateTime(exam_date, QTime(0, 0))
        self.display_number = display_number
        
        self.initUI()
        self.start_countdown()

    def initUI(self):
        # Set window flags for always-on-top and no frame
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        
        # Make the window transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create the countdown label with modern styling
        self.countdown_label = QLabel(self)
        self.countdown_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);
            color: red;
            padding: 10px;
            border-radius: 15px;
        """)
        
        # Use a different, modern font: Arial
        font = QFont("Arial", 24)
        self.countdown_label.setFont(font)
        
        # Position the window on the specified display
        self.position_window()
        self.show()

    def position_window(self):
        screens = QApplication.screens()
        
        # Check if the requested display number exists
        if len(screens) > self.display_number - 1:
            target_screen = screens[self.display_number - 1]
            screen_geometry = target_screen.availableGeometry()
            
            # Use a realistic sample text for sizing
            self.countdown_label.setText("1000d 00h 00m 00s")
            self.countdown_label.adjustSize()
            label_size = self.countdown_label.size()
            
            # Calculate the position
            x = screen_geometry.x() + screen_geometry.width() - label_size.width()
            y = screen_geometry.y() + 30
            
            self.move(x, y)
            self.setFixedSize(label_size)
        else:
            print(f"Error: Display number {self.display_number} not found. Defaulting to primary display.")
            primary_screen = QApplication.primaryScreen()
            screen_geometry = primary_screen.availableGeometry()
            
            self.countdown_label.setText("1000d 00h 00m 00s")
            self.countdown_label.adjustSize()
            label_size = self.countdown_label.size()
            
            x = screen_geometry.width() - label_size.width()
            y = 45
            
            self.move(x, y)
            self.setFixedSize(label_size)
    
    def update_countdown(self):
        now = QDateTime.currentDateTime()
        seconds_to_go = now.secsTo(self.exam_datetime)
        
        if seconds_to_go > 0:
            # Calculate and format the remaining time
            days = seconds_to_go // 86400
            hours = (seconds_to_go % 86400) // 3600
            minutes = (seconds_to_go % 3600) // 60
            seconds = seconds_to_go % 60
            
            # Update the label text with a more concise format
            self.countdown_label.setText(f"{days}d {hours:02}h {minutes:02}m {seconds:02}s")
        else:
            self.timer.stop()
            self.countdown_label.setText("EXAM DAY!")
            self.countdown_label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 150);
                color: red;
                padding: 10px;
                border-radius: 15px;
            """)
        
        # Adjust the window size to fit the new text
        self.countdown_label.adjustSize()
        self.setFixedSize(self.countdown_label.size())

    def start_countdown(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)
        self.update_countdown()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Your A/L Exam Date: August 10, 2026
    sri_lankan_al_exam_date = QDate(2026, 8, 10)
    
    # To use the second display, pass 2 as the argument
    # To use the first display, pass 1
    countdown = CountdownOverlay(sri_lankan_al_exam_date, display_number=1)
    sys.exit(app.exec())
