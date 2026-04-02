# Email Automation TUI

A terminal user interface for managing email automation profiles.

## Features

- **View Profiles**: Browse all configured email profiles with status indicators
- **Create Profile**: Add new email automation profiles with:
  - Sender email(s)
  - Receiver email(s)
  - Email subject
  - Email body/content
  - Conditions (date/time based)
- **Manage Profiles**: Edit, delete, or duplicate existing profiles
- **Activate/Deactivate**: Control which profiles are running
- **Status Monitoring**: View active profiles and their status
- **Import/Export**: Save and load profiles from JSON files
- **Backend Integration**: Direct communication with the Python backend via multiprocessing queues

## Usage

**Standalone mode:**
```bash
python tui/main.py
```

**With backend integration:**
```bash
python main.py
```

## Available Commands

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `list` | List all profiles with status |
| `view <id>` | View detailed profile information |
| `create` | Create a new profile interactively |
| `edit <id>` | Edit an existing profile |
| `delete <id>` | Delete a profile |
| `duplicate <id>` | Create a copy of a profile |
| `activate <id>` | Activate a profile to start sending emails |
| `deactivate <id>` | Stop an active profile |
| `status` | Show active profiles and count |
| `export [filename]` | Export profiles to JSON (default: profiles_export.json) |
| `import <filename>` | Import profiles from JSON file |
| `clear` | Clear all profiles (requires confirmation) |
| `exit` / `quit` | Exit the application |

## Architecture

- **Standard Library Only**: No external dependencies required for core functionality
- **Queue-based Communication**: Uses multiprocessing queues to communicate with backend
- **Command Prompt Style**: Clean, simple terminal interface like Windows CMD

## Profile Storage

Profiles are stored in `.profiles.json` in the working directory:

```json
{
  "profile-uuid": {
    "sender_emails": ["sender@gmail.com"],
    "receiver_emails": ["recipient@example.com"],
    "password": "app-password",
    "topic": "Email Subject",
    "email_content": "Email body content",
    "condition": 0
  }
}
```

## Conditions

Conditions determine when emails are sent:
- `0`: Send immediately
- `1+`: Date/time based conditions (See `backend/conditions.py`)

## Profile Status

- `●` (filled circle) = Active profile
- `○` (empty circle) = Inactive profile

## Integration with Backend

The TUI integrates with the backend's multiprocessing system:
- Sends commands via request queue
- Receives responses via response queue
- Automatically logs actions to `.log.log`

## Future Enhancements

- [ ] Profile scheduling interface
- [ ] Email preview before sending
- [ ] Condition builder UI
- [ ] Color support with `rich` library
- [ ] Real-time queue monitoring
- [ ] Profile templates

