# phone-agent

Control your Android phone hands-free with natural language — powered by Claude AI and Droidrun.

A US-adapted fork of [DDalkkak](https://github.com/aristoapp/DDalkkak) by aristoapp, rebuilt for US-based services (Uber Eats, Amazon, etc.).

<video src="uber_eats.mp4" controls width="600"></video>

---

## What it does

Type a command like `order me KFC` and the agent opens Uber Eats on your physical Android phone, navigates the UI, and places the order — no hands, no taps.

---

## Stack

| Layer | Tech |
|---|---|
| AI / Intent parsing | [Claude API](https://www.anthropic.com) (claude-sonnet) |
| Android automation | [Droidrun](https://docs.droidrun.ai) SDK + Portal app |
| Device communication | ADB (Android Debug Bridge) |
| Runtime | Python 3.12+, [uv](https://github.com/astral-sh/uv) |

---

## How it works

```
User input → Claude (intent parsing) → Router → Service Handler
    → Droidrun Agent → ADB → Android phone (no touch needed)
```

---

## Setup

### 1. Prerequisites

- macOS with [Homebrew](https://brew.sh)
- Android phone with USB debugging enabled
- Anthropic API key

### 2. Install ADB

```bash
brew install android-platform-tools
```

### 3. Connect your phone

Enable **Developer Options** on your phone (tap Build Number 7 times), then enable **USB Debugging**. Connect via USB and accept the trust prompt.

```bash
adb devices  # confirm your device shows up
```

### 4. Install dependencies

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --python 3.12
```

### 5. Install Droidrun Portal on your phone

Download the latest APK from [droidrun-portal releases](https://github.com/droidrun/droidrun-portal/releases) and install:

```bash
adb install -r com.droidrun.portal-x.x.x-debug.apk
```

Then open the Portal app and enable the **Accessibility Service** when prompted.

```bash
PATH="/opt/homebrew/bin:$PATH" uv run droidrun ping  # should return OK
```

### 6. Configure environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
DEVICE_SERIAL=YOUR_DEVICE_SERIAL   # from `adb devices`
```

---

## Run

```bash
PATH="/opt/homebrew/bin:$PATH" uv run python -m src.main
```

---

## Example commands

```
order me KFC
can you order me Subway?
order a pizza from Domino's
```

> Known restaurant names (KFC, McDonald's, Subway, etc.) bypass the Claude API entirely for faster execution.

