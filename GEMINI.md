# gemini-ntfy

**gemini-ntfy** is a Gemini CLI extension that integrates with [ntfy.sh](https://ntfy.sh) to send push notifications to your device when the Gemini agent finishes a task or requires your attention.

## Project Overview

*   **Type:** Gemini CLI Extension
*   **Language:** Python 3 (Hook script)
*   **Key Dependencies:** `ntfy.sh` (external service), Python standard library (no external pip packages required).
*   **Purpose:** To provide mobile/desktop alerts for long-running CLI agent tasks.

## Architecture

The extension works by hooking into Gemini's event system:

1.  **Configuration (`gemini-extension.json`):** Defines the extension metadata, available settings, and points to the hook configuration.
2.  **Hook Definition (`hooks/hooks.json`):** Maps Gemini events (`AfterAgent`, `Notification`) to the executable script.
3.  **Hook Implementation (`hooks/ntfy_hook.py`):** A standalone Python script that:
    *   Reads configuration from environment variables.
    *   Parses the event data passed via `stdin` (JSON).
    *   Sends an HTTP POST request to the configured `ntfy.sh` server/topic.

## Configuration & Usage

### Settings

The extension is configured via environment variables, typically set using `gemini extensions config gemini-ntfy`.

*   `GEMINI_NTFY_TOPIC` (Required): The ntfy topic name. **Treat this like a password.**
*   `GEMINI_NTFY_SERVER`: The ntfy server URL. Defaults to `https://ntfy.sh`.
*   `GEMINI_NTFY_ID`: Unique ID for notification threading. Defaults to the system hostname.
*   `GEMINI_NTFY_CLICK`: URL/Intent to open on click. Defaults to opening Termux on Android.

### Events

*   **`AfterAgent`**: Triggered when the agent completes a session. Sends a summary of the response.
*   **`Notification`**: Triggered when the agent explicitly requests user attention (e.g., input needed).

## Development & Release

### File Structure

*   `gemini-extension.json`: Manifest file.
*   `hooks/hooks.json`: Event-to-command mapping.
*   `hooks/ntfy_hook.py`: Main logic script.
*   `.github/workflows/auto-release.yml`: CI workflow.

### Release Process

This project uses an automated release workflow:

1.  **Mandatory Version Bump:** You MUST update the `"version"` field in `gemini-extension.json` whenever any changes are made to the extension logic or hooks.
2.  **Commit and Push:** Commit the changes (including the version bump) and push to `main`.
3.  **Automatic Release:** GitHub Actions will detect the version change, tag the commit, and publish a GitHub Release automatically.
