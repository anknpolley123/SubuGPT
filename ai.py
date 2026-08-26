import sys
import os
import platform
import time
import json
import requests
from datetime import datetime


# ============================================================
# DEPENDENCIES
# ============================================================

def install_package(package):
    os.system(
        f"{sys.executable} -m pip install {package} --quiet"
    )


try:
    import pyfiglet
except ImportError:
    install_package("pyfiglet")
    import pyfiglet


try:
    from langdetect import detect
except ImportError:
    install_package("langdetect")
    from langdetect import detect


try:
    import requests
except ImportError:
    install_package("requests")
    import requests


# ============================================================
# COLORS
# ============================================================

class colors:
    black = "\033[0;30m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    blue = "\033[0;34m"
    purple = "\033[0;35m"
    cyan = "\033[0;36m"
    white = "\033[0;37m"

    bright_black = "\033[1;30m"
    bright_red = "\033[1;31m"
    bright_green = "\033[1;32m"
    bright_yellow = "\033[1;33m"
    bright_blue = "\033[1;34m"
    bright_purple = "\033[1;35m"
    bright_cyan = "\033[1;36m"
    bright_white = "\033[1;37m"

    reset = "\033[0m"
    bold = "\033[1m"


# ============================================================
# CONFIGURATION
# ============================================================

CONFIG_FILE = "subugpt_config.json"

# IMPORTANT:
# Your existing system prompt file.
PROMPT_FILE = "system-prompt.txt"

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"

# OpenRouter's free-model router
DEFAULT_MODEL = "openrouter/free"

SITE_URL = "https://github.com/anknpolley123/SubuGPT"
SITE_NAME = "SubuGPT CLI"

SUPPORTED_LANGUAGES = [
    "English",
    "Indonesian",
    "Spanish",
    "Arabic",
    "Thai",
    "Portuguese"
]


# ============================================================
# FILE PATH
# ============================================================

# Always look for system-prompt.txt in the same directory
# as this Python script.
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROMPT_PATH = os.path.join(
    BASE_DIR,
    PROMPT_FILE
)


# ============================================================
# CONFIGURATION FUNCTIONS
# ============================================================

def load_config():

    default_config = {
        "base_url": DEFAULT_BASE_URL,
        "model": DEFAULT_MODEL,
        "language": "English"
    }

    if not os.path.exists(CONFIG_FILE):
        return default_config

    try:
        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            config = json.load(f)

        # Restore missing settings
        for key, value in default_config.items():

            if key not in config:
                config[key] = value

        return config

    except Exception:
        return default_config


def save_config(config):

    try:

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                config,
                f,
                indent=2
            )

    except Exception as e:

        print(
            f"{colors.red}"
            f"Could not save configuration: {e}"
            f"{colors.reset}"
        )


# ============================================================
# SCREEN
# ============================================================

def clear_screen():

    os.system(
        "cls"
        if platform.system() == "Windows"
        else "clear"
    )


# ============================================================
# BANNER
# ============================================================

def banner():

    try:

        figlet = pyfiglet.Figlet(
            font="big"
        )

        print(
            f"{colors.bright_red}"
            f"{figlet.renderText('SubuGPT')}"
            f"{colors.reset}"
        )

    except Exception:

        print(
            f"{colors.bright_red}"
            "SubuGPT"
            f"{colors.reset}"
        )

    print(
        f"{colors.bright_red}"
        "SubuGPT CLI"
        f"{colors.reset}"
    )

    print(
        f"{colors.bright_cyan}"
        "OpenRouter API | "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"{colors.reset}"
    )

    print(
        f"{colors.bright_cyan}"
        "Developed by Ankon Polley <3"
        f"{colors.reset}"
    )

    print(
        f"{colors.bright_red}"
        f"{SITE_URL}"
        f"{colors.reset}\n"
    )


# ============================================================
# TYPING EFFECT
# ============================================================

def typing_print(
    text,
    delay=0.01
):

    for char in text:

        sys.stdout.write(char)
        sys.stdout.flush()

        time.sleep(delay)

    print()


# ============================================================
# LANGUAGE SELECTION
# ============================================================

def select_language():

    config = load_config()

    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ Language Selection ]"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"Current: "
        f"{colors.green}{config['language']}"
        f"{colors.reset}"
    )

    for index, language in enumerate(
        SUPPORTED_LANGUAGES,
        start=1
    ):

        print(
            f"{colors.green}"
            f"{index}. {language}"
            f"{colors.reset}"
        )

    while True:

        try:

            choice = int(
                input(
                    f"\n{colors.red}"
                    "[>] Select "
                    f"(1-{len(SUPPORTED_LANGUAGES)}): "
                    f"{colors.reset}"
                )
            )

            if (
                1
                <= choice
                <= len(SUPPORTED_LANGUAGES)
            ):

                config["language"] = (
                    SUPPORTED_LANGUAGES[
                        choice - 1
                    ]
                )

                save_config(config)

                print(
                    f"{colors.bright_cyan}"
                    "Language set to "
                    f"{config['language']}"
                    f"{colors.reset}"
                )

                time.sleep(1)

                return

            print(
                f"{colors.red}"
                "Invalid selection!"
                f"{colors.reset}"
            )

        except ValueError:

            print(
                f"{colors.red}"
                "Please enter a number."
                f"{colors.reset}"
            )


# ============================================================
# MODEL SELECTION
# ============================================================

def select_model():

    config = load_config()

    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ Model Configuration ]"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"Current: "
        f"{colors.green}{config['model']}"
        f"{colors.reset}"
    )

    print(
        f"\n{colors.yellow}"
        "1. Enter custom model ID"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        "2. Use OpenRouter Free Router"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        "3. Back to menu"
        f"{colors.reset}"
    )

    while True:

        choice = input(
            f"\n{colors.red}"
            "[>] Select (1-3): "
            f"{colors.reset}"
        )

        if choice == "1":

            new_model = input(
                f"{colors.red}"
                "Enter model ID: "
                f"{colors.reset}"
            ).strip()

            if new_model:

                config["model"] = new_model

                save_config(config)

                print(
                    f"{colors.bright_cyan}"
                    "Model updated."
                    f"{colors.reset}"
                )

                time.sleep(1)

                return

        elif choice == "2":

            config["model"] = DEFAULT_MODEL

            save_config(config)

            print(
                f"{colors.bright_cyan}"
                f"Model set to {DEFAULT_MODEL}"
                f"{colors.reset}"
            )

            time.sleep(1)

            return

        elif choice == "3":

            return

        else:

            print(
                f"{colors.red}"
                "Invalid choice!"
                f"{colors.reset}"
            )


# ============================================================
# SYSTEM PROMPT
# ============================================================

def get_system_prompt():

    """
    Read the existing system-prompt.txt file.

    IMPORTANT:
    This function NEVER creates or overwrites the file.

    The file must be located in the same directory
    as ai.py.
    """

    try:

        with open(
            PROMPT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            prompt = f.read().strip()

        if not prompt:

            return (
                "[System prompt is empty. "
                "Please add instructions to "
                "system-prompt.txt]"
            )

        return prompt

    except FileNotFoundError:

        return (
            "[System prompt file not found]\n\n"
            f"Expected file:\n{PROMPT_PATH}\n\n"
            "Create system-prompt.txt in the same "
            "folder as ai.py."
        )

    except PermissionError:

        return (
            "[System prompt error]\n\n"
            "Permission denied while reading:\n"
            f"{PROMPT_PATH}"
        )

    except Exception as e:

        return (
            "[System prompt error]\n\n"
            f"{e}"
        )


# ============================================================
# API KEY
# ============================================================

def get_api_key():

    """
    Read the OpenRouter API key from the
    OPENROUTER_API_KEY environment variable.

    The key is NOT stored in subugpt_config.json.
    """

    return os.getenv(
        "OPENROUTER_API_KEY"
    )


# ============================================================
# API REQUEST
# ============================================================

def call_api(user_input):

    config = load_config()

    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    api_key = get_api_key()

    if not api_key:

        return (
            "[SubuGPT] API Error:\n\n"
            "OPENROUTER_API_KEY is not set.\n\n"
            "Run:\n"
            "export OPENROUTER_API_KEY='YOUR_API_KEY'"
        )

    # --------------------------------------------------------
    # LANGUAGE DETECTION
    # --------------------------------------------------------

    try:

        detected = detect(
            user_input[:500]
        )

        language_map = {

            "id": "Indonesian",
            "en": "English",
            "es": "Spanish",
            "ar": "Arabic",
            "th": "Thai",
            "pt": "Portuguese"

        }

        detected_language = language_map.get(
            detected,
            "English"
        )

        if (
            detected_language
            != config["language"]
        ):

            config["language"] = (
                detected_language
            )

            save_config(config)

    except Exception:

        pass

    # --------------------------------------------------------
    # LOAD SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = get_system_prompt()

    # --------------------------------------------------------
    # HEADERS
    # --------------------------------------------------------

    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "HTTP-Referer":
            SITE_URL,

        "X-Title":
            SITE_NAME,

        "Content-Type":
            "application/json"
    }

    # --------------------------------------------------------
    # REQUEST DATA
    # --------------------------------------------------------

    data = {

        "model":
            config["model"],

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_input
            }

        ],

        "max_tokens":
            500,

        "temperature":
            0.7
    }

    # --------------------------------------------------------
    # SEND REQUEST
    # --------------------------------------------------------

    try:

        response = requests.post(

            f"{config['base_url']}"
            "/chat/completions",

            headers=headers,

            json=data,

            timeout=120
        )

        # ----------------------------------------------------
        # API ERROR
        # ----------------------------------------------------

        if not response.ok:

            try:

                error_data = response.json()

                error_object = (
                    error_data.get(
                        "error",
                        {}
                    )
                )

                error_message = (
                    error_object.get(
                        "message",
                        response.text
                    )
                )

                return (
                    f"[SubuGPT] API Error "
                    f"{response.status_code}:\n"
                    f"{error_message}"
                )

            except Exception:

                return (
                    f"[SubuGPT] API Error "
                    f"{response.status_code}:\n"
                    f"{response.text}"
                )

        # ----------------------------------------------------
        # PARSE RESPONSE
        # ----------------------------------------------------

        result = response.json()

        choices = result.get(
            "choices",
            []
        )

        if not choices:

            return (
                "[SubuGPT] API returned "
                "no choices."
            )

        message = choices[0].get(
            "message",
            {}
        )

        content = message.get(
            "content"
        )

        if not content:

            return (
                "[SubuGPT] The model returned "
                "an empty response."
            )

        return content

    except requests.exceptions.Timeout:

        return (
            "[SubuGPT] Request timed out."
        )

    except requests.exceptions.ConnectionError:

        return (
            "[SubuGPT] Could not connect "
            "to OpenRouter."
        )

    except requests.exceptions.RequestException as e:

        return (
            f"[SubuGPT] Network error:\n{e}"
        )

    except Exception as e:

        return (
            f"[SubuGPT] API Error:\n{e}"
        )


# ============================================================
# CHAT SESSION
# ============================================================

def chat_session():

    config = load_config()

    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ Chat Session ]"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"Model: "
        f"{colors.green}{config['model']}"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        "Commands: menu | clear | exit"
        f"{colors.reset}"
    )

    while True:

        try:

            user_input = input(
                f"\n{colors.red}"
                "[SubuGPT]~[#]> "
                f"{colors.reset}"
            )

            if not user_input.strip():

                continue

            command = (
                user_input
                .strip()
                .lower()
            )

            # ------------------------------------------------
            # EXIT
            # ------------------------------------------------

            if command == "exit":

                print(
                    f"{colors.bright_cyan}"
                    "Exiting..."
                    f"{colors.reset}"
                )

                sys.exit(0)

            # ------------------------------------------------
            # MENU
            # ------------------------------------------------

            elif command == "menu":

                return

            # ------------------------------------------------
            # CLEAR
            # ------------------------------------------------

            elif command == "clear":

                clear_screen()

                banner()

                print(
                    f"{colors.bright_cyan}"
                    "[ Chat Session ]"
                    f"{colors.reset}"
                )

                continue

            # ------------------------------------------------
            # AI REQUEST
            # ------------------------------------------------

            response = call_api(
                user_input
            )

            if response:

                print(
                    f"\n{colors.bright_cyan}"
                    "Response:"
                    f"{colors.reset}\n"
                    f"{colors.white}",
                    end=""
                )

                typing_print(
                    response
                )

        except KeyboardInterrupt:

            print(
                f"\n{colors.red}"
                "Interrupted!"
                f"{colors.reset}"
            )

            return

        except Exception as e:

            print(
                f"\n{colors.red}"
                f"Error: {e}"
                f"{colors.reset}"
            )


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    while True:

        config = load_config()

        clear_screen()
        banner()

        print(
            f"{colors.bright_cyan}"
            "[ Main Menu ]"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            f"1. Language: "
            f"{colors.green}"
            f"{config['language']}"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            f"2. Model: "
            f"{colors.green}"
            f"{config['model']}"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            "3. Start Chat"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            "4. Exit"
            f"{colors.reset}"
        )

        try:

            choice = input(
                f"\n{colors.red}"
                "[>] Select (1-4): "
                f"{colors.reset}"
            )

            if choice == "1":

                select_language()

            elif choice == "2":

                select_model()

            elif choice == "3":

                chat_session()

            elif choice == "4":

                print(
                    f"{colors.bright_cyan}"
                    "Exiting..."
                    f"{colors.reset}"
                )

                sys.exit(0)

            else:

                print(
                    f"{colors.red}"
                    "Invalid selection!"
                    f"{colors.reset}"
                )

                time.sleep(1)

        except KeyboardInterrupt:

            print(
                f"\n{colors.red}"
                "Interrupted!"
                f"{colors.reset}"
            )

            sys.exit(1)

        except Exception as e:

            print(
                f"\n{colors.red}"
                f"Error: {e}"
                f"{colors.reset}"
            )

            time.sleep(2)


# ============================================================
# MAIN
# ============================================================

def main():

    # Create configuration only.
    # NEVER create or overwrite system-prompt.txt.

    if not os.path.exists(
        CONFIG_FILE
    ):

        save_config({

            "base_url":
                DEFAULT_BASE_URL,

            "model":
                DEFAULT_MODEL,

            "language":
                "English"
        })

    # Warn if system-prompt.txt is missing.
    if not os.path.exists(
        PROMPT_PATH
    ):

        print(
            f"{colors.yellow}"
            "WARNING: system-prompt.txt was not found."
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            f"Expected location:\n{PROMPT_PATH}"
            f"{colors.reset}\n"
        )

        time.sleep(2)

    try:

        main_menu()

    except KeyboardInterrupt:

        print(
            f"\n{colors.red}"
            "Interrupted! Exiting..."
            f"{colors.reset}"
        )

    except Exception as e:

        print(
            f"\n{colors.red}"
            f"Fatal error: {e}"
            f"{colors.reset}"
        )

        sys.exit(1)


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()

