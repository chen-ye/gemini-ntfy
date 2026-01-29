# Gemini Ntfy Notifier

This extension sends notifications via [ntfy.sh](https://ntfy.sh) when the Gemini agent needs attention or finishes a task.

## Configuration

The extension uses the following environment variables:

- `GEMINI_NTFY_TOPIC`: The topic to subscribe to (default: `gemini_alerts` passed as arg, or set via env).
- `GEMINI_NTFY_SERVER`: The ntfy server URL (default: `https://ntfy.sh`).
- `GEMINI_NTFY_ID`: Unique ID for updating notifications (default: hostname).

## Hooks

- **AfterAgent**: Sends a notification with the agent's final response.
- **Notification**: Sends a notification when the agent manually requests attention (e.g. asking for input).