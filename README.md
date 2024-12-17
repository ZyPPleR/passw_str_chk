# Password Strength Checker and Suggestion Tool

## Overview
The Password Strength Checker and Suggestion Tool is a Python application designed to:
- Analyze the strength of user-entered passwords dynamically.
- Provide feedback and suggestions for improving password strength.
- Check passwords against known breaches using the Have I Been Pwned API.
- Generate secure passwords with customizable options.
- Allow switching between light and dark themes.
- Offer tips for creating strong passwords.

## Features
- **Dynamic Password Strength Analysis:**
  - Automatically evaluates password strength as you type.
  - Displays a score (Very Weak to Very Strong) and improvement suggestions.

- **Breach Check Integration:**
  - Verifies if the password has been compromised in data breaches.
  - Uses the Have I Been Pwned API to ensure password safety.

- **Secure Password Generation:**
  - Generate random secure passwords.
  - Advanced customization for length and character types (uppercase, digits, special characters).

- **User-Friendly Interface:**
  - Includes a toggle for password visibility.
  - Provides theme switching (Light/Dark mode).

- **Helpful Tips:**
  - Offers guidelines on creating strong, secure passwords.

## Requirements
Ensure you have the following installed:
- Python 3.7 or higher
- Required Python libraries:
  - PyQt5
  - zxcvbn
  - requests

## Installation
1. **Download our project and open it in Visual Studio Code or in another program of its type.**

2. **Install the required dependencies:**
   ```bash
   pip install PyQt5 zxcvbn requests
   ```

3. **If you get a PSReadline warning in the terminal. That:**
    - Try to update it via the terminal:
    ```bash
    Update-Module PSReadline
    ```
    - If you don't have it, download it by writing in the terminal (before that, run the program with administrator rights): 
    ```bash
    Install-Module -Force PSReadline 
    ```
## Usage
1. **Run the code.**

2. **Password Input:**
   - Enter your password in the provided input field.
   - Password strength will update dynamically as you type.

3. **Breach Check:**
   - Click "Check Password Breach" to verify if your password has been exposed in a data breach.

4. **Generate Password:**
   - Use "Generate Secure Password" for quick password creation.
   - For advanced options, click "Advanced Password Generation."

5. **Theme Switching:**
   - Toggle between light and dark themes using the "Switch to Dark Theme" button.

6. **Tips:**
   - Click "Show Tips for Strong Passwords" for guidelines on creating secure passwords.

## Acknowledgements
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [zxcvbn](https://github.com/dropbox/zxcvbn) for password strength analysis.

### THANK YOU FOR DOWNLOADING OUR PROJECT!