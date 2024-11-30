This script is a Telegram bot that translates text between multiple languages using the Google Translate API.
The user can specify the source and target languages along with the text to be translated.
For educational purposes only. Unauthorized or illegal use is strictly prohibite

# Installation

# Installation and Setup Instructions

Follow these steps to set up the project:

1. Update the system:

    ```bash
    apt update && apt upgrade -y
    ```

2. Update Termux packages:

    ```bash
    pkg update && pkg upgrade -y
    ```

3. Install Python and Git:

    ```bash
    pkg install python
    ```
    ```bash
    pkg install python3
    ```
    ```bash
    pkg install git
    ```

4. Clone the repository:

    ```bash
    git clone https://github.com/SCSEA/g-trans.git
    ```

5. Navigate to the project directory:

    ```bash
    cd g-trans
    ```

6. Install required Python modules:

    ```bash
    pip install -r requirements.txt
    ```
    ```bash
    pip install pyTelegramBotAPI
    ```
    ```bash
    pip install requests
    ```
    ```bash
    pip install colorama
    ```

    For Python3:
    ```bash
    pip3 install pyTelegramBotAPI
    ```
    ```bash
    pip3 install requests
    ```
    ```bash
    pip3 install colorama
    ```

7. Run the script:

    ```bash
    python google-trans.py
    ```

    or use Python3:

    ```bash
    python3 google-trans.py
    ```

---

### Note:
Make sure to enter your Telegram Bot API Token in the script before running the program.


![Visitor Count](https://komarev.com/ghpvc/?username=SCSEA&color=green)

