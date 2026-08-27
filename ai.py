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
API_KEY_FILE = "subugpt_api_key.txt"  # New file for API key storage

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

API_KEY_PATH = os.path.join(
    BASE_DIR,
    API_KEY_FILE
)


# ============================================================
# CONFIGURATION FUNCTIONS
# ============================================================

def load_config():
    default_config = {
        "base_url": DEFAULT_BASE_URL,
        "model": DEFAULT_MODEL,
        "language": "English",
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
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
# API KEY MANAGEMENT
# ============================================================

def get_api_key():
    """
    Read the OpenRouter API key from:
    1. Environment variable OPENROUTER_API_KEY (preferred)
    2. API key file (subugpt_api_key.txt)
    """
    # First check environment variable
    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key:
        return env_key

    # Then check the API key file
    try:
        if os.path.exists(API_KEY_PATH):
            with open(API_KEY_PATH, "r", encoding="utf-8") as f:
                key = f.read().strip()
                if key:
                    return key
    except Exception:
        pass

    return None


def save_api_key(api_key):
    """Save API key to file"""
    try:
        # Save to file with secure permissions
        with open(API_KEY_PATH, "w", encoding="utf-8") as f:
            f.write(api_key.strip())
        
        # Set secure permissions (Unix-like systems only)
        if platform.system() != "Windows":
            os.chmod(API_KEY_PATH, 0o600)
        
        return True
    except Exception as e:
        print(
            f"{colors.red}"
            f"Error saving API key: {e}"
            f"{colors.reset}"
        )
        return False


def delete_api_key():
    """Delete the stored API key"""
    try:
        if os.path.exists(API_KEY_PATH):
            os.remove(API_KEY_PATH)
            return True
        return False
    except Exception as e:
        print(
            f"{colors.red}"
            f"Error deleting API key: {e}"
            f"{colors.reset}"
        )
        return False


def set_api_key():
    """Interactive API key setup"""
    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ API Key Management ]"
        f"{colors.reset}\n"
    )

    current_key = get_api_key()
    if current_key:
        # Mask the key for display
        masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "********"
        print(
            f"{colors.green}"
            f"Current API Key: {masked_key}"
            f"{colors.reset}\n"
        )
    else:
        print(
            f"{colors.yellow}"
            "No API key found."
            f"{colors.reset}\n"
        )

    print(
        f"{colors.cyan}"
        "You can get your OpenRouter API key from:\n"
        "https://openrouter.ai/keys"
        f"{colors.reset}\n"
    )

    print(
        f"{colors.yellow}"
        "Options:"
        f"{colors.reset}"
    )
    print(
        f"{colors.green}"
        "1. Set API key from file"
        f"{colors.reset}"
    )
    print(
        f"{colors.green}"
        "2. Enter API key manually"
        f"{colors.reset}"
    )
    print(
        f"{colors.green}"
        "3. Use environment variable (OPENROUTER_API_KEY)"
        f"{colors.reset}"
    )
    if current_key:
        print(
            f"{colors.red}"
            "4. Delete stored API key"
            f"{colors.reset}"
        )
    print(
        f"{colors.green}"
        "5. Back to menu"
        f"{colors.reset}"
    )

    while True:
        try:
            choice = input(
                f"\n{colors.red}"
                "[>] Select (1-5): "
                f"{colors.reset}"
            )

            if choice == "1":
                file_path = input(
                    f"{colors.red}"
                    "Enter path to API key file: "
                    f"{colors.reset}"
                ).strip()

                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            key = f.read().strip()
                            if key:
                                if save_api_key(key):
                                    print(
                                        f"{colors.bright_green}"
                                        "API key saved successfully!"
                                        f"{colors.reset}"
                                    )
                                    time.sleep(1)
                                    return
                            else:
                                print(
                                    f"{colors.red}"
                                    "File is empty!"
                                    f"{colors.reset}"
                                )
                    except Exception as e:
                        print(
                            f"{colors.red}"
                            f"Error reading file: {e}"
                            f"{colors.reset}"
                        )
                else:
                    print(
                        f"{colors.red}"
                        "File not found!"
                        f"{colors.reset}"
                    )
                time.sleep(1)

            elif choice == "2":
                print(
                    f"{colors.yellow}"
                    "Enter your OpenRouter API key:"
                    f"{colors.reset}"
                )
                api_key = input(
                    f"{colors.red}"
                    "[>] "
                    f"{colors.reset}"
                ).strip()

                if api_key:
                    # Validate key format (basic check)
                    if len(api_key) >= 20:
                        if save_api_key(api_key):
                            print(
                                f"{colors.bright_green}"
                                "API key saved successfully!"
                                f"{colors.reset}"
                            )
                            time.sleep(1)
                            return
                    else:
                        print(
                            f"{colors.red}"
                            "Invalid API key format. Key should be at least 20 characters."
                            f"{colors.reset}"
                        )
                        time.sleep(1)
                else:
                    print(
                        f"{colors.red}"
                        "API key cannot be empty!"
                        f"{colors.reset}"
                    )
                    time.sleep(1)

            elif choice == "3":
                env_key = os.getenv("OPENROUTER_API_KEY")
                if env_key:
                    print(
                        f"{colors.bright_green}"
                        "Environment variable is set."
                        f"{colors.reset}"
                    )
                    # Optionally save to file as well
                    save_env = input(
                        f"{colors.yellow}"
                        "Save this key to file for future use? (y/n): "
                        f"{colors.reset}"
                    ).strip().lower()
                    if save_env == "y":
                        if save_api_key(env_key):
                            print(
                                f"{colors.bright_green}"
                                "API key saved to file!"
                                f"{colors.reset}"
                            )
                else:
                    print(
                        f"{colors.red}"
                        "OPENROUTER_API_KEY environment variable is not set."
                        f"{colors.reset}"
                    )
                    print(
                        f"{colors.yellow}"
                        "To set it, run:\n"
                        f"export OPENROUTER_API_KEY='your_api_key_here'"
                        f"{colors.reset}"
                    )
                time.sleep(2)

            elif choice == "4" and current_key:
                confirm = input(
                    f"{colors.red}"
                    "Are you sure you want to delete the stored API key? (y/n): "
                    f"{colors.reset}"
                ).strip().lower()
                if confirm == "y":
                    if delete_api_key():
                        print(
                            f"{colors.bright_green}"
                            "API key deleted successfully!"
                            f"{colors.reset}"
                        )
                        time.sleep(1)
                        return
                else:
                    print(
                        f"{colors.yellow}"
                        "Deletion cancelled."
                        f"{colors.reset}"
                    )
                    time.sleep(1)

            elif choice == "5":
                return

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
                "Cancelled."
                f"{colors.reset}"
            )
            return

        except Exception as e:
            print(
                f"{colors.red}"
                f"Error: {e}"
                f"{colors.reset}"
            )
            time.sleep(1)


def view_api_key_status():
    """Display API key status"""
    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ API Key Status ]"
        f"{colors.reset}\n"
    )

    key = get_api_key()
    if key:
        masked_key = key[:8] + "..." + key[-4:] if len(key) > 12 else "********"
        print(
            f"{colors.bright_green}"
            f"✓ API Key is set"
            f"{colors.reset}"
        )
        print(
            f"{colors.cyan}"
            f"Key: {masked_key}"
            f"{colors.reset}"
        )
        
        # Check if key is stored in file or environment
        if os.getenv("OPENROUTER_API_KEY"):
            print(
                f"{colors.cyan}"
                "Source: Environment variable (OPENROUTER_API_KEY)"
                f"{colors.reset}"
            )
        elif os.path.exists(API_KEY_PATH):
            print(
                f"{colors.cyan}"
                f"Source: File ({API_KEY_FILE})"
                f"{colors.reset}"
            )
    else:
        print(
            f"{colors.bright_red}"
            "✗ No API Key found"
            f"{colors.reset}"
        )
        print(
            f"{colors.yellow}"
            "Please set your API key using option 7 in the main menu."
            f"{colors.reset}"
        )

    print()
    input(
        f"{colors.yellow}"
        "Press Enter to continue..."
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
        "SubuGPT API | "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"{colors.reset}"
    )

    print(
        f"{colors.bright_cyan}"
        "Developed by Ankon Polley👨‍💻"
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
        "3. View available models"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        "4. Back to menu"
        f"{colors.reset}"
    )

    while True:
        choice = input(
            f"\n{colors.red}"
            "[>] Select (1-4): "
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
            view_available_models()

        elif choice == "4":
            return

        else:
            print(
                f"{colors.red}"
                "Invalid choice!"
                f"{colors.reset}"
            )


# ============================================================
# VIEW AVAILABLE MODELS
# ============================================================

def view_available_models():
    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ Available Models ]"
        f"{colors.reset}"
    )

    try:
        # Get models from OpenRouter
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            timeout=30
        )

        if response.ok:
            data = response.json()
            models = data.get("data", [])

            # Sort models by name
            models.sort(key=lambda x: x.get("id", ""))

            # Display models in paginated format
            page_size = 10
            total_pages = (len(models) + page_size - 1) // page_size
            current_page = 0

            while True:
                clear_screen()
                banner()
                print(
                    f"{colors.bright_cyan}"
                    f"[ Available Models - Page {current_page + 1}/{total_pages} ]"
                    f"{colors.reset}\n"
                )

                start_idx = current_page * page_size
                end_idx = min(start_idx + page_size, len(models))

                for i in range(start_idx, end_idx):
                    model = models[i]
                    model_id = model.get("id", "Unknown")
                    context_length = model.get("context_length", "N/A")
                    pricing = model.get("pricing", {})
                    prompt_price = pricing.get("prompt", "N/A")
                    completion_price = pricing.get("completion", "N/A")

                    print(
                        f"{colors.green}{i + 1}. {colors.white}{model_id}"
                        f"{colors.reset}"
                    )
                    print(
                        f"{colors.cyan}   Context: {context_length} | "
                        f"Prompt: ${prompt_price} | "
                        f"Completion: ${completion_price}"
                        f"{colors.reset}\n"
                    )

                print(
                    f"{colors.yellow}"
                    "Commands: [n]ext | [p]revious | [s]elect | [b]ack"
                    f"{colors.reset}"
                )

                cmd = input(
                    f"\n{colors.red}"
                    "[>] "
                    f"{colors.reset}"
                ).strip().lower()

                if cmd == "n" and current_page < total_pages - 1:
                    current_page += 1
                elif cmd == "p" and current_page > 0:
                    current_page -= 1
                elif cmd == "s":
                    try:
                        model_num = int(input(
                            f"{colors.red}"
                            "Enter model number: "
                            f"{colors.reset}"
                        ))

                        if 1 <= model_num <= len(models):
                            selected_model = models[model_num - 1]
                            config = load_config()
                            config["model"] = selected_model.get("id")
                            save_config(config)

                            print(
                                f"{colors.bright_cyan}"
                                f"Model set to {config['model']}"
                                f"{colors.reset}"
                            )
                            time.sleep(1)
                            return
                    except ValueError:
                        print(
                            f"{colors.red}"
                            "Invalid number!"
                            f"{colors.reset}"
                        )
                        time.sleep(1)
                elif cmd == "b":
                    return

        else:
            print(
                f"{colors.red}"
                "Could not fetch models from OpenRouter."
                f"{colors.reset}"
            )
            time.sleep(2)

    except Exception as e:
        print(
            f"{colors.red}"
            f"Error fetching models: {e}"
            f"{colors.reset}"
        )
        time.sleep(2)


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
            "Set your API key using:\n"
            "1. Environment variable: export OPENROUTER_API_KEY='YOUR_API_KEY'\n"
            "2. Or use the 'Set API Key' option in the main menu"
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
            config.get("max_tokens", 500),
        "temperature":
            config.get("temperature", 0.7),
        "top_p":
            config.get("top_p", 1.0),
        "frequency_penalty":
            config.get("frequency_penalty", 0.0),
        "presence_penalty":
            config.get("presence_penalty", 0.0)
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

                # Check for authentication errors
                if response.status_code == 401:
                    return (
                        f"[SubuGPT] Authentication Error:\n\n"
                        f"Invalid API key.\n\n"
                        f"Please check your API key using:\n"
                        f"1. Environment variable: OPENROUTER_API_KEY\n"
                        f"2. Or use the 'Set API Key' option in the main menu"
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
        "Commands: menu | clear | exit | save [filename] | load [filename]"
        f"{colors.reset}"
    )

    chat_history = []

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
            # SAVE CHAT HISTORY
            # ------------------------------------------------

            elif command.startswith("save "):
                filename = user_input[5:].strip()
                if filename:
                    try:
                        with open(filename, "w", encoding="utf-8") as f:
                            json.dump(chat_history, f, indent=2)
                        print(
                            f"{colors.bright_green}"
                            f"Chat saved to {filename}"
                            f"{colors.reset}"
                        )
                    except Exception as e:
                        print(
                            f"{colors.red}"
                            f"Error saving chat: {e}"
                            f"{colors.reset}"
                        )
                continue

            # ------------------------------------------------
            # LOAD CHAT HISTORY
            # ------------------------------------------------

            elif command.startswith("load "):
                filename = user_input[5:].strip()
                if filename and os.path.exists(filename):
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            chat_history = json.load(f)
                        print(
                            f"{colors.bright_green}"
                            f"Chat loaded from {filename}"
                            f"{colors.reset}"
                        )
                    except Exception as e:
                        print(
                            f"{colors.red}"
                            f"Error loading chat: {e}"
                            f"{colors.reset}"
                        )
                else:
                    print(
                        f"{colors.red}"
                        f"File not found: {filename}"
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
                # Add to chat history
                chat_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "assistant": response
                })

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
# ADVANCED SETTINGS
# ============================================================

def advanced_settings():
    config = load_config()

    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ Advanced Settings ]"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"1. Max Tokens: "
        f"{colors.green}{config.get('max_tokens', 500)}"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"2. Temperature: "
        f"{colors.green}{config.get('temperature', 0.7)}"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"3. Top P: "
        f"{colors.green}{config.get('top_p', 1.0)}"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"4. Frequency Penalty: "
        f"{colors.green}{config.get('frequency_penalty', 0.0)}"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        f"5. Presence Penalty: "
        f"{colors.green}{config.get('presence_penalty', 0.0)}"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        "6. Reset to defaults"
        f"{colors.reset}"
    )

    print(
        f"{colors.yellow}"
        "7. Back to menu"
        f"{colors.reset}"
    )

    while True:
        choice = input(
            f"\n{colors.red}"
            "[>] Select (1-7): "
            f"{colors.reset}"
        )

        if choice == "1":
            try:
                value = float(input(
                    f"{colors.red}"
                    "Enter max tokens (1-4096): "
                    f"{colors.reset}"
                ))
                if 1 <= value <= 4096:
                    config["max_tokens"] = int(value)
                    save_config(config)
                    print(
                        f"{colors.bright_cyan}"
                        "Setting updated."
                        f"{colors.reset}"
                    )
                    time.sleep(1)
                    return
            except ValueError:
                print(
                    f"{colors.red}"
                    "Invalid input!"
                    f"{colors.reset}"
                )
                time.sleep(1)

        elif choice == "2":
            try:
                value = float(input(
                    f"{colors.red}"
                    "Enter temperature (0-2): "
                    f"{colors.reset}"
                ))
                if 0 <= value <= 2:
                    config["temperature"] = value
                    save_config(config)
                    print(
                        f"{colors.bright_cyan}"
                        "Setting updated."
                        f"{colors.reset}"
                    )
                    time.sleep(1)
                    return
            except ValueError:
                print(
                    f"{colors.red}"
                    "Invalid input!"
                    f"{colors.reset}"
                )
                time.sleep(1)

        elif choice == "3":
            try:
                value = float(input(
                    f"{colors.red}"
                    "Enter top p (0-1): "
                    f"{colors.reset}"
                ))
                if 0 <= value <= 1:
                    config["top_p"] = value
                    save_config(config)
                    print(
                        f"{colors.bright_cyan}"
                        "Setting updated."
                        f"{colors.reset}"
                    )
                    time.sleep(1)
                    return
            except ValueError:
                print(
                    f"{colors.red}"
                    "Invalid input!"
                    f"{colors.reset}"
                )
                time.sleep(1)

        elif choice == "4":
            try:
                value = float(input(
                    f"{colors.red}"
                    "Enter frequency penalty (-2 to 2): "
                    f"{colors.reset}"
                ))
                if -2 <= value <= 2:
                    config["frequency_penalty"] = value
                    save_config(config)
                    print(
                        f"{colors.bright_cyan}"
                        "Setting updated."
                        f"{colors.reset}"
                    )
                    time.sleep(1)
                    return
            except ValueError:
                print(
                    f"{colors.red}"
                    "Invalid input!"
                    f"{colors.reset}"
                )
                time.sleep(1)

        elif choice == "5":
            try:
                value = float(input(
                    f"{colors.red}"
                    "Enter presence penalty (-2 to 2): "
                    f"{colors.reset}"
                ))
                if -2 <= value <= 2:
                    config["presence_penalty"] = value
                    save_config(config)
                    print(
                        f"{colors.bright_cyan}"
                        "Setting updated."
                        f"{colors.reset}"
                    )
                    time.sleep(1)
                    return
            except ValueError:
                print(
                    f"{colors.red}"
                    "Invalid input!"
                    f"{colors.reset}"
                )
                time.sleep(1)

        elif choice == "6":
            confirm = input(
                f"{colors.red}"
                "Reset all advanced settings to defaults? (y/n): "
                f"{colors.reset}"
            ).strip().lower()
            if confirm == "y":
                config["max_tokens"] = 500
                config["temperature"] = 0.7
                config["top_p"] = 1.0
                config["frequency_penalty"] = 0.0
                config["presence_penalty"] = 0.0
                save_config(config)
                print(
                    f"{colors.bright_cyan}"
                    "Settings reset to defaults."
                    f"{colors.reset}"
                )
                time.sleep(1)
                return

        elif choice == "7":
            return

        else:
            print(
                f"{colors.red}"
                "Invalid selection!"
                f"{colors.reset}"
            )
            time.sleep(1)


# ============================================================
# VIEW SYSTEM PROMPT
# ============================================================

def view_system_prompt():
    clear_screen()
    banner()

    print(
        f"{colors.bright_cyan}"
        "[ System Prompt ]"
        f"{colors.reset}\n"
    )

    prompt = get_system_prompt()
    print(
        f"{colors.white}"
        f"{prompt}"
        f"{colors.reset}\n"
    )

    input(
        f"{colors.yellow}"
        "Press Enter to continue..."
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

        # Show API key status in menu
        api_key = get_api_key()
        api_status = f"{colors.green}✓ Set" if api_key else f"{colors.red}✗ Not Set"
        
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
            f"3. API Key: "
            f"{api_status}"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            "4. Start Chat"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            "5. Advanced Settings"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            "6. View System Prompt"
            f"{colors.reset}"
        )

        print(
            f"{colors.yellow}"
            "7. Exit"
            f"{colors.reset}"
        )

        try:
            choice = input(
                f"\n{colors.red}"
                "[>] Select (1-7): "
                f"{colors.reset}"
            )

            if choice == "1":
                select_language()

            elif choice == "2":
                select_model()

            elif choice == "3":
                set_api_key()

            elif choice == "4":
                # Check if API key is set before starting chat
                if not get_api_key():
                    print(
                        f"{colors.red}"
                        "Please set your API key first (option 3)!"
                        f"{colors.reset}"
                    )
                    time.sleep(2)
                    continue
                chat_session()

            elif choice == "5":
                advanced_settings()

            elif choice == "6":
                view_system_prompt()

            elif choice == "7":
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
                "English",
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
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

    # Check API key status on startup
    api_key = get_api_key()
    if not api_key:
        print(
            f"{colors.yellow}"
            "No API key found. Please set it using option 3 in the main menu."
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