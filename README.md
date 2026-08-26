# 🐛 SubuGPT CLI - OpenRouter Edition

**SubuGPT CLI** is a sleek command-line interface (CLI) for interacting with LLMs via OpenRouter API. It supports multiple models, automatic language detection, and customizable settings — all in a terminal-friendly format.

> ⚡ Lightweight. Powerful. Fully terminal-based. Developed by [@anknpolley123](https://github.com/anknpolley123)

---

## 🚀 Features

- 🔗 OpenRouter API integration
- 🌍 Auto language detection (via `langdetect`)
- 🗣️ Multi-language support: English, Indonesian, Spanish, Arabic, Thai, Portuguese
- 💬 Interactive chat session with typing effect
- 🎨 Stylish CLI UI with colors and banners
- 🔧 Easy configuration of API key and model
- 💾 Config auto-saved in `subugpt_config.json`

---

## 📦 Requirements

- Python 3.6+
- `pip` installed
- OpenRouter API key ([get one here](https://openrouter.ai/))

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/anknpolley123/SubuGPT
cd SubuGPT
```

## Setup

```bash
#create virtual environment 

# Then Install all Requirements

pip install -r requirements.txt 

# Set Your Api At kali

export OPENROUTER_API_KEY="Your api key"

# Run command for validating api key

python3 op.py
```
Open Config File

```bash
{
  "api_key": "Paste Your API Key",
  "base_url": "https://openrouter.ai/api/v1",
  "model": "openrouter/free",
  "language": "English"
}
```

### If you get this message 

```bash
┌──(Ankon)(kali㉿localhost)-[~/SubuGPT]
└─$ python3 op.py
Quantum computing uses quantum bits (qubits) that can exist in superposition and become entangled, allowing a quantum computer to process many possibilities simultaneously and solve certain problems exponentially faster than classical computers.
```
You succeed

## 🧠 After Setup Run this commad to use it

```
python3 ai.py
```

## Menu will appear:

```
[ Main Menu ]
1. Language: English
2. Model: deepseek/deepseek-chat-v3-0324:free
3. Set API Key
4. Start Chat
5. Exit
```

## 🧪 Custom Models

From the menu, you can enter your own model ID (from OpenRouter).

Example:
```
01-ai/Yi-34B-Chat
meta-llama/llama-3-8b-instruct:nitro
```

### 📷 Example Screenshot
![SubuGPT CLI Example](assets/Screenshot_20260825_234703_Termux.jpg)

## 👨‍💻 Author

GitHub: @anknpolley123

Instagram: @its_an_geun_woo

Project URL: https://github.com/anknpolley123/SubuGPT