import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar
import yt_dlp
import re 

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YouTube Video Downloader (yt-dlp)")
        self.setGeometry(400, 200, 400, 250)
        
        layout = QVBoxLayout()

        # Label and input field for YouTube URL
        self.label = QLabel("Enter YouTube URL:")
        layout.addWidget(self.label)
        
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        layout.addWidget(self.url_input)
        
        # Progress bar for download progress
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Download button 
        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        self.setLayout(layout)
        
    def download_video(self):
        url = self.url_input.text().strip()
        
        if not url.startswith("https://www.youtube.com/") and not url.startswith("https://youtu.be/"):
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid YouTube URL.")
            return
        
        # Get the Downloads folder path on device
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # yt-dlp options to download video in the Downloads folder with progress hook
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Saves file as <Downloads>/<video_title>.mp4
            'progress_hooks': [self.progress_hook],  # Hook for download progress
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, "Success", "Video downloaded successfully!")
            self.progress_bar.setValue(0)  # Reset progress bar after download
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Get the percentage completed with ANSI codes removed
            percentage_str = d.get('_percent_str', '0%')
            percentage_str = re.sub(r'\x1b\[[0-9;]*m', '', percentage_str)  # Remove ANSI escape sequences
            percentage = int(float(percentage_str.strip('%')))  # Convert to int
            
            self.progress_bar.setValue(percentage)  # Set integer value

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = YouTubeDownloader()
    downloader.show()
    sys.exit(app.exec_())
