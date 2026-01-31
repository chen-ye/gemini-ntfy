# Gemini Ntfy Notifier

This extension sends notifications via [ntfy.sh](https://ntfy.sh) when the Gemini agent needs attention or finishes a task.

## Installation

```bash
gemini extensions install https://github.com/chen-ye/gemini-ntfy.git
```

## Requirements

- **Python 3.x**: The hook script is written in Python and requires a Python 3 interpreter available on the system path.

## Configuration

You can configure this extension using the following command:

```bash
gemini extensions config gemini-ntfy
```

Available settings:

- **Ntfy Topic** (`GEMINI_NTFY_TOPIC`): The topic to subscribe to.
  - **IMPORTANT**: ntfy.sh topics are public by default. Treat your topic name like a password (e.g., use a long random string) to prevent others from reading your notifications.
- **Ntfy Server** (`GEMINI_NTFY_SERVER`): The ntfy server URL (default: `https://ntfy.sh`).
- **Ntfy ID** (`GEMINI_NTFY_ID`): Unique ID for updating notifications (default: hostname).
- **Click Action** (`GEMINI_NTFY_CLICK`): The URL or intent to open when the notification is clicked.
  - **Note**: This defaults to `intent://#Intent;package=com.termux;end` which opens the **Termux** app on Android.

## Hooks

- **AfterAgent**: Sends a notification with the agent's final response.
- **Notification**: Sends a notification when the agent manually requests attention (e.g. asking for input).