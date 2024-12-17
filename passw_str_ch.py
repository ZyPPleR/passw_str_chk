from PyQt5 import QtWidgets, QtGui, QtCore
from zxcvbn import zxcvbn
import random
import string
import hashlib
import requests
import sys
import json

class PasswordCheckerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Strength Checker")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        #Main layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self.layout)

        #Theme toggle button
        self.theme_button = QtWidgets.QPushButton("Switch to Dark Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_button)

        #Input field for password
        password_layout = QtWidgets.QHBoxLayout()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.textChanged.connect(self.update_strength_indicator)
        password_layout.addWidget(self.password_input)

        #Toggle password visibility button
        self.toggle_password_button = QtWidgets.QPushButton("Show")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.toggled.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_password_button)

        self.layout.addLayout(password_layout)

        #Password strength progress bar
        self.strength_progress = QtWidgets.QProgressBar()
        self.strength_progress.setMaximum(4)  # zxcvbn scores from 0 to 4
        self.strength_progress.setTextVisible(True)
        self.layout.addWidget(self.strength_progress)

        #Strength result display
        self.strength_label = QtWidgets.QLabel("Password strength will be shown here")
        self.strength_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.strength_label)

        #Button to check password breach
        self.breach_button = QtWidgets.QPushButton("Check Password Breach")
        self.breach_button.clicked.connect(self.check_password_breach)
        self.layout.addWidget(self.breach_button)

        #Generate secure password
        self.generate_button = QtWidgets.QPushButton("Generate Secure Password")
        self.generate_button.clicked.connect(self.generate_secure_password)
        self.layout.addWidget(self.generate_button)

        #Generated password display
        self.generated_password_label = QtWidgets.QLineEdit()
        self.generated_password_label.setReadOnly(True)
        self.generated_password_label.setPlaceholderText("Generated password will appear here")
        self.layout.addWidget(self.generated_password_label)

        #Export results
        self.export_button = QtWidgets.QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button)

        #Advanced password generation
        self.advanced_button = QtWidgets.QPushButton("Advanced Password Generation")
        self.advanced_button.clicked.connect(self.advanced_password_generation)
        self.layout.addWidget(self.advanced_button)

        #Tips for strong passwords
        self.tips_button = QtWidgets.QPushButton("Show Tips for Strong Passwords")
        self.tips_button.clicked.connect(self.show_password_tips)
        self.layout.addWidget(self.tips_button)

    #Toggles the application theme between light and dark mode.
    #-Light mode uses the default system appearance.
    #-Dark mode changes the background to dark gray and text to white.
    #Triggered by the "Switch to Dark Theme" button.
    def toggle_theme(self):
        if self.theme_button.text() == "Switch to Dark Theme":
            self.setStyleSheet("""
                background-color: #2E2E2E;
                color: #D3D3D3;  
                font-family: Segoe UI;
                font-size: 14px;
            """)
            self.theme_button.setText("Switch to Light Theme")
        else:
            self.setStyleSheet("""
                background-color: #FFFFFF;
                color: #000000;  
                font-family: Segoe UI;
                font-size: 12px;
            """)
            self.theme_button.setText("Switch to Dark Theme")


    #Displays a dialog with tips for creating strong passwords.
    #-Tips include length, character variety, and avoiding common patterns.
    #Triggered by the "Show Tips for Strong Passwords" button.
    def show_password_tips(self):
        tips = (
            "1. Use at least 12 characters.\n"
            "2. Include uppercase and lowercase letters.\n"
            "3. Add numbers and special characters.\n"
            "4. Avoid common words and predictable patterns.\n"
            "5. Use a unique password for each account."
        )
        QtWidgets.QMessageBox.information(self, "Tips for Strong Passwords", tips)
    
    #Toggles the visibility of the password input field.
    #-If toggled on, the password becomes visible, and the button text changes to "Hide".
    #-If toggled off, the password is hidden, and the button text changes to "Show".
    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.toggle_password_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
            self.toggle_password_button.setText("Show")

    #Dynamically updates the strength indicator as the user types in the password.
    #-Uses zxcvbn to calculate a score (0 to 4) and provide feedback.
    #-Updates the progress bar and displays suggestions for improving the password.
    #This replaces the need for a separate "Check Password Strength" button.
    def update_strength_indicator(self):
        password = self.password_input.text()
        if not password:
            self.strength_progress.setValue(0)
            self.strength_progress.setFormat("Very Weak")
            self.strength_label.setText("Password strength will be shown here")
            return

        try:
            result = zxcvbn(password)
            score = result['score']
            feedback = result['feedback']['suggestions']

            strength_text = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
            self.strength_progress.setValue(score)
            self.strength_progress.setFormat(strength_text[score])
            self.strength_label.setText(f"Strength: {strength_text[score]}\n" + "\n".join(feedback))
        except Exception:
            self.strength_progress.setValue(0)
            self.strength_progress.setFormat("Error")
            self.strength_label.setText("Error analyzing password strength.")

    #Checks if the entered password has been exposed in data breaches using Have I Been Pwned API.
    #-Hashes the password with SHA-1 and sends the first 5 characters of the hash to the API.
    #-Compares the rest of the hash with the API response to determine if the password is compromised.
    #Displays the result: "Password found in breaches" or "Password not found in breaches".
    def check_password_breach(self):
        password = self.password_input.text()
        if not password:
            self.strength_label.setText("Please enter a password.")
            return

        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_password[:5]
        suffix = sha1_password[5:]

        try:
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url)

            if response.status_code != 200:
                self.strength_label.setText("Error connecting to API.")
                return

            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    self.strength_label.setText(f"Password found in {count} breaches. Change it immediately!")
                    return

            self.strength_label.setText("Password not found in breaches. Good to go!")
        except requests.RequestException:
            self.strength_label.setText("Network error. Check your internet connection.")

    #Generates a random secure password with a fixed length of 12 characters.
    #-Includes uppercase letters, lowercase letters, digits, and special characters.
    #Displays the generated password in a read-only field.
    def generate_secure_password(self):
        characters = string.ascii_letters + string.digits + "!@#$%^&*()-_+=<>?/|"
        password = ''.join(random.choices(characters, k=12))
        self.generated_password_label.setText(password)

    #Opens the advanced password generation dialog.
    #-Allows the user to customize password length and character types (uppercase, digits, special characters).
    #The generated password appears in the dialog window.
    def advanced_password_generation(self):
        dialog = AdvancedPasswordDialog(self)
        dialog.exec_()

    #Exports the password analysis results to a file in JSON or plain text format.
    #-Prompts the user to select a file location and format.
    #-Saves the password, strength score, and breach check result.
    #Displays a success or error message based on the operation's outcome.
    def export_results(self):
        password = self.password_input.text()
        if not password:
            self.strength_label.setText("Please enter a password to export results.")
            return

        try:
            result = {
                "password": password,
                "strength": self.strength_progress.format(),
                "breach_check": self.strength_label.text()
            }

            options = QtWidgets.QFileDialog.Options()
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Results", "", "JSON Files (*.json);;Text Files (*.txt)", options=options)

            if file_path:
                with open(file_path, 'w') as file:
                    if file_path.endswith('.json'):
                        json.dump(result, file, indent=4)
                    else:
                        file.write(f"Password: {result['password']}\n")
                        file.write(f"Strength: {result['strength']}\n")
                        file.write(f"Breach Check: {result['breach_check']}\n")
                self.strength_label.setText("Results exported successfully.")
        except Exception as e:
            self.strength_label.setText(f"Error exporting results: {str(e)}")

class AdvancedPasswordDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Password Generation")
        self.setGeometry(150, 150, 400, 300)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Убирает значок вопроса
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        #Length input
        self.length_label = QtWidgets.QLabel("Password Length:")
        layout.addWidget(self.length_label)

        self.length_input = QtWidgets.QSpinBox()
        self.length_input.setMinimum(8)
        self.length_input.setMaximum(64)
        self.length_input.setValue(12)
        layout.addWidget(self.length_input)

        #Checkbox for character types
        self.include_uppercase = QtWidgets.QCheckBox("Include Uppercase Letters")
        self.include_uppercase.setChecked(True)
        layout.addWidget(self.include_uppercase)

        self.include_digits = QtWidgets.QCheckBox("Include Digits")
        self.include_digits.setChecked(True)
        layout.addWidget(self.include_digits)

        self.include_special = QtWidgets.QCheckBox("Include Special Characters")
        self.include_special.setChecked(True)
        layout.addWidget(self.include_special)

        #Generate button
        self.generate_button = QtWidgets.QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        #Result display
        self.result_display = QtWidgets.QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Generated password will appear here")
        layout.addWidget(self.result_display)

    def generate_password(self):
        length = self.length_input.value()
        characters = string.ascii_lowercase

        if self.include_uppercase.isChecked():
            characters += string.ascii_uppercase
        if self.include_digits.isChecked():
            characters += string.digits
        if self.include_special.isChecked():
            characters += "!@#$%^&*()-_+=<>?/|"

        password = ''.join(random.choices(characters, k=length))
        self.result_display.setText(password)

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        main_window = PasswordCheckerApp()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")