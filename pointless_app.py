import sys
import random
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QProgressBar, QTextEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush

# --- Worker Thread for "Complex" Background Tasks ---
# This class handles the fake analysis without freezing the UI.
# It emits signals to the main window to update different widgets.
class AnalysisWorker(QObject):
    """
    A worker that runs in a separate thread to simulate a complex,
    time-consuming analysis. It communicates with the main UI thread
    via signals.
    """
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)
    visualizer_updated = pyqtSignal()
    analysis_complete = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_running = True

    def run(self):
        """The main logic of the worker thread."""
        self.log_updated.emit("Initializing quantum flux capacitor...")
        time.sleep(0.5)
        self.log_updated.emit("Calibrating harmonic resonance matrix...")
        time.sleep(0.5)

        # Simulate a long-running process
        for i in range(101):
            if not self.is_running:
                self.log_updated.emit("Analysis aborted by user.")
                return

            # Update progress bar
            self.progress_updated.emit(i)

            # Update the quantum visualizer randomly
            if i % 2 == 0:
                self.visualizer_updated.emit()

            # Add nonsensical log messages at random intervals
            if random.random() < 0.1:
                log_messages = [
                    "Re-routing primary data stream...",
                    "Defragmenting neutrino buffer...",
                    "Compiling sub-etheric protocols...",
                    "Warning: Tachyon particle surge detected.",
                    "Engaging Heisenberg compensator...",
                    "Matrix alignment at 74%...",
                    "ERROR: Reality integrity questionable. Continuing anyway.",
                ]
                self.log_updated.emit(random.choice(log_messages))

            time.sleep(random.uniform(0.05, 0.15))

        self.log_updated.emit("Analysis complete. Collapsing waveform.")
        
        # Generate a final, completely useless verdict
        final_verdicts = [
            "Verdict: The data suggests a high probability of ambiguity.",
            "Verdict: Outcome inconclusive. Recommend consulting a psychic.",
            "Verdict: A superposition of 'yes' and 'no' has been achieved.",
            "Verdict: The signal-to-noise ratio is suboptimal for a conclusion.",
            "Verdict: All signs point to 'maybe'.",
            "Verdict: The query has been successfully ignored.",
        ]
        self.analysis_complete.emit(random.choice(final_verdicts))

    def stop(self):
        self.is_running = False

# --- Custom Widget for the "Quantum Visualizer" ---
# A grid of colored cells that flash randomly to look impressive.
class QuantumVisualizer(QWidget):
    """
    A custom widget that displays a grid of randomly colored squares
    to simulate a complex data visualization.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 20
        self.colors = [[self.get_random_color() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.setMinimumSize(200, 200)

    def get_random_color(self):
        """Returns a random QColor, biased towards dark greens and greys."""
        if random.random() < 0.7:
            return QColor(0, random.randint(50, 150), 0, random.randint(50, 150))
        return QColor(random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))

    def update_grid(self):
        """Regenerates the colors for the grid and triggers a repaint."""
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if random.random() < 0.2: # Only update some cells for a "live" feel
                    self.colors[r][c] = self.get_random_color()
        self.update() # Schedule a repaint

    def paintEvent(self, event):
        """Paints the grid of colored cells."""
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        
        cell_width = self.width() / self.grid_size
        cell_height = self.height() / self.grid_size

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                painter.setBrush(QBrush(self.colors[r][c]))
                painter.drawRect(int(c * cell_width), int(r * cell_height), int(cell_width), int(cell_height))


# --- The Main Application Window ---
class PointlessApp(QMainWindow):
    """
    The main window of the application, bringing all the unnecessarily
    complex widgets together.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Hyper-Encabulator Matrix")
        self.setGeometry(100, 100, 800, 600)

        # Apply a dark, "high-tech" stylesheet
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: #00ff7f;
                font-family: 'Courier New', Courier, monospace;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                background-color: #0d0d0d;
                border: 1px solid #00ff7f;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #00ff7f;
                color: #000000;
                border: none;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QProgressBar {
                border: 1px solid #00ff7f;
                border-radius: 5px;
                text-align: center;
                color: #1a1a1a;
                background-color: #0d0d0d;
            }
            QProgressBar::chunk {
                background-color: #00ff7f;
                border-radius: 4px;
            }
        """)

        # --- Main Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Left Panel (Controls) ---
        left_panel_layout = QVBoxLayout()
        
        self.input_label = QLabel("Enter Data for Encabulation:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., 'Should I get a coffee?'")
        
        self.analyze_button = QPushButton("ENGAGE ENCABULATOR")
        self.analyze_button.clicked.connect(self.start_analysis)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.final_verdict_label = QLabel("Verdict: Awaiting Input...")
        self.final_verdict_label.setWordWrap(True)
        self.final_verdict_label.setFont(QFont('Courier New', 16, QFont.Weight.Bold))
        self.final_verdict_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_panel_layout.addWidget(self.input_label)
        left_panel_layout.addWidget(self.input_field)
        left_panel_layout.addSpacing(20)
        left_panel_layout.addWidget(self.analyze_button)
        left_panel_layout.addSpacing(20)
        left_panel_layout.addWidget(self.progress_bar)
        left_panel_layout.addSpacing(20)
        left_panel_layout.addWidget(self.final_verdict_label)
        left_panel_layout.addStretch()

        # --- Right Panel (Data Display) ---
        right_panel_layout = QVBoxLayout()
        
        self.visualizer_label = QLabel("Quantum State Visualizer:")
        self.visualizer = QuantumVisualizer()
        
        self.log_label = QLabel("Analysis Log:")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        
        right_panel_layout.addWidget(self.visualizer_label)
        right_panel_layout.addWidget(self.visualizer, 1) # Give it more stretch
        right_panel_layout.addWidget(self.log_label)
        right_panel_layout.addWidget(self.log_output, 1) # Give it more stretch

        # --- Combine Panels ---
        main_layout.addLayout(left_panel_layout, 1)
        main_layout.addLayout(right_panel_layout, 2)

        self.worker_thread = None
        self.worker = None

    def start_analysis(self):
        """Handles the 'Engage' button click."""
        # This check is now safe because self.worker_thread is None
        # if the previous thread has finished and been cleaned up.
        if self.worker_thread and self.worker_thread.isRunning():
            return

        # Reset UI elements
        self.progress_bar.setValue(0)
        self.log_output.clear()
        self.final_verdict_label.setText("Verdict: Encabulating...")
        self.analyze_button.setDisabled(True)
        self.analyze_button.setText("ENCABULATING...")

        # Set up and start the worker thread
        self.worker_thread = QThread()
        self.worker = AnalysisWorker()
        self.worker.moveToThread(self.worker_thread)

        # Connect signals from worker to slots in the main window
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.log_updated.connect(self.log_output.append)
        self.worker.visualizer_updated.connect(self.visualizer.update_grid)
        self.worker.analysis_complete.connect(self.on_analysis_complete)
        
        # Connect thread lifecycle signals
        self.worker_thread.started.connect(self.worker.run)
        # When the thread finishes, schedule the worker object for deletion
        self.worker_thread.finished.connect(self.worker.deleteLater)
        # NEW: Connect the finished signal to our cleanup slot
        self.worker_thread.finished.connect(self.on_thread_finished)
        
        self.worker_thread.start()

    def on_analysis_complete(self, verdict):
        """Called when the worker's task is done. This runs in the main thread."""
        self.final_verdict_label.setText(verdict)
        self.analyze_button.setDisabled(False)
        self.analyze_button.setText("ENGAGE ENCABULATOR")
        
        # The worker's job is done, so we can tell the thread to quit its event loop.
        # This will eventually emit the 'finished' signal.
        if self.worker_thread:
            self.worker_thread.quit()

    def on_thread_finished(self):
        """
        NEW: This slot is called when the thread has finished its event loop.
        It's now safe to discard our references to the thread and worker.
        """
        self.worker_thread = None
        self.worker = None
        self.log_output.append("\nSystem ready for next analysis.")

    def closeEvent(self, event):
        """Ensures the worker thread is stopped when the window closes."""
        if self.worker:
            self.worker.stop()
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait() # Wait for thread to finish
        event.accept()


# --- Application Entry Point ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PointlessApp()
    window.show()
    sys.exit(app.exec())
