import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from multiprocessing import Queue
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "python_backend"
sys.path.insert(0, str(backend_path))

try:
    from profiles import create_profile, delete_profile, edit_profile
    from utils import read_profiles, log_action
    from conditions import send_email_on
except ImportError as e:
    print(f"Warning: Could not import backend modules: {e}")


class EmailAutomationTUI:
    def __init__(self, request_queue: Optional[Queue] = None, response_queue: Optional[Queue] = None):
        self.profiles_file = Path(".profiles.json")
        self.profiles: Dict[str, Dict[str, Any]] = self.load_profiles()
        self.running = True
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.active_profiles: Dict[str, bool] = {}  # Track which profiles are running
        self.commands = {
            "help": "Show available commands",
            "list": "List all profiles",
            "view": "View profile details (view <id>)",
            "create": "Create a new profile",
            "edit": "Edit a profile (edit <id>)",
            "delete": "Delete a profile (delete <id>)",
            "duplicate": "Duplicate a profile (duplicate <id>)",
            "export": "Export profiles to JSON (export <filename>)",
            "import": "Import profiles from JSON (import <filename>)",
            "activate": "Activate a profile (activate <id>)",
            "deactivate": "Deactivate a profile (deactivate <id>)",
            "status": "Show active profiles",
            "clear": "Clear all profiles (WARNING)",
            "exit": "Exit the application",
            "quit": "Exit the application"
        }
        
    def load_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Load profiles from .profiles.json"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_profiles(self) -> None:
        """Save profiles to .profiles.json"""
        with open(self.profiles_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)
    
    def print_header(self) -> None:
        """Print TUI header/title"""
        print("\nEmail Automation > ", end="", flush=True)
    
    def show_help(self) -> None:
        """Show all available commands"""
        print("\nAvailable Commands:")
        print("-" * 50)
        for cmd, desc in self.commands.items():
            print(f"  {cmd:<15} - {desc}")
        print("-" * 50)
    
    def get_multiline_input(self, prompt: str) -> str:
        """Get multiline input (Enter twice to finish)"""
        print(f"{prompt} (Enter twice to finish):")
        lines = []
        empty_count = 0
        while True:
            try:
                line = input("> ").strip()
                if not line:
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break
        return "\n".join(lines)
    
    def get_email_list(self) -> List[str]:
        """Get a list of emails from user (comma or line separated)"""
        response = input("Emails (comma or newline separated): ").strip()
        emails = []
        if "," in response:
            emails = [e.strip() for e in response.split(",")]
        else:
            emails = [e.strip() for e in response.split("\n")]
        return [e for e in emails if e]
    
    def display_profile(self, profile_id: str, profile: Dict[str, Any]) -> None:
        """Display a single profile"""
        status = "ACTIVE" if self.active_profiles.get(profile_id) else "INACTIVE"
        print(f"\nProfile ID: {profile_id}")
        print(f"  Status:     [{status}]")
        print(f"  Senders:    {', '.join(profile.get('sender_emails', []))}")
        print(f"  Recipients: {', '.join(profile.get('receiver_emails', []))}")
        print(f"  Subject:    {profile.get('topic', 'N/A')}")
        print(f"  Content:    {profile.get('email_content', 'N/A')[:60]}...")
        print(f"  Condition:  {profile.get('condition', 0)}")
    
    def list_profiles(self) -> None:
        """List all profiles with status"""
        if not self.profiles:
            print("No profiles found. Use 'create' to add one.")
            return
        
        print(f"\n{len(self.profiles)} profile(s):")
        print("-" * 60)
        for profile_id, profile in self.profiles.items():
            subject = profile.get('topic', 'Untitled')
            status = "●" if self.active_profiles.get(profile_id) else "○"
            print(f"  {status} {profile_id[:8]}... - {subject}")
        print("-" * 60)
    
    def view_profile(self, profile_id: str) -> None:
        """View detailed profile information"""
        if profile_id not in self.profiles:
            print(f"Error: Profile '{profile_id}' not found.")
            return
        
        self.display_profile(profile_id, self.profiles[profile_id])
    
    def show_status(self) -> None:
        """Show status of active profiles"""
        active_count = sum(1 for v in self.active_profiles.values() if v)
        print(f"\nStatus: {active_count}/{len(self.profiles)} profiles active")
        
        if active_count > 0:
            print("\nActive profiles:")
            for profile_id, is_active in self.active_profiles.items():
                if is_active and profile_id in self.profiles:
                    print(f"  • {profile_id[:8]}... - {self.profiles[profile_id].get('topic', 'Untitled')}")
        else:
            print("No active profiles")
    
    def execute_create(self) -> None:
        """Create a new profile interactively"""
        print("\n--- Create New Profile ---")
        
        sender_emails_str = input("Sender email(s) (comma-separated): ").strip()
        sender_emails = [e.strip() for e in sender_emails_str.split(",") if e.strip()]
        
        if not sender_emails:
            print("Error: At least one sender email required.")
            return
        
        recipient_str = input("Recipient email(s) (comma-separated): ").strip()
        recipient_emails = [e.strip() for e in recipient_str.split(",") if e.strip()]
        
        if not recipient_emails:
            print("Error: At least one recipient email required.")
            return
        
        password = input("Email password: ").strip()
        subject = input("Subject: ").strip()
        content = self.get_multiline_input("Content")
        condition = input("Condition ID (default 0): ").strip() or "0"
        
        try:
            condition_int = int(condition)
        except ValueError:
            condition_int = 0
        
        try:
            new_profile = create_profile(
                sender_emails=sender_emails,
                receiver_emails=recipient_emails,
                password=password,
                topic=subject,
                email_content=content,
                condition=condition_int
            )
            
            self.profiles.update(new_profile)
            self.save_profiles()
            
            profile_id = list(new_profile.keys())[0]
            print(f"Profile created: {profile_id}")
            
            # Log action if available
            if self.request_queue:
                log_action(f"Profile created: {profile_id}")
                self.request_queue.put({
                    'message': 'add profile',
                    'data': (sender_emails, recipient_emails, password, subject, content, condition_int)
                })
        except Exception as e:
            print(f"Error creating profile: {e}")
    
    def execute_edit(self, profile_id: str) -> None:
        """Edit an existing profile"""
        if profile_id not in self.profiles:
            print(f"Error: Profile '{profile_id}' not found.")
            return
        
        profile = self.profiles[profile_id]
        print(f"\nEditing: {profile_id}")
        print("(Leave blank to keep current value)")
        
        senders_str = input(f"Senders [{', '.join(profile['sender_emails'])}]: ").strip()
        if senders_str:
            profile['sender_emails'] = [e.strip() for e in senders_str.split(",")]
        
        recipients_str = input(f"Recipients [{', '.join(profile['receiver_emails'])}]: ").strip()
        if recipients_str:
            profile['receiver_emails'] = [e.strip() for e in recipients_str.split(",")]
        
        password = input("Password: ").strip()
        if password:
            profile['password'] = password
        
        topic = input(f"Subject [{profile['topic']}]: ").strip()
        if topic:
            profile['topic'] = topic
        
        content = input(f"Content [{profile['email_content'][:30]}...]: ").strip()
        if content:
            profile['email_content'] = content
        
        condition = input(f"Condition [{profile['condition']}]: ").strip()
        if condition:
            try:
                profile['condition'] = int(condition)
            except ValueError:
                pass
        
        self.save_profiles()
        print("Profile updated.")
    
    def execute_delete(self, profile_id: str) -> None:
        """Delete a profile"""
        if profile_id not in self.profiles:
            print(f"Error: Profile '{profile_id}' not found.")
            return
        
        confirm = input(f"Delete {profile_id[:8]}...? (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                del self.profiles[profile_id]
                self.active_profiles.pop(profile_id, None)
                self.save_profiles()
                print("Profile deleted.")
                
                if self.request_queue:
                    self.request_queue.put({'message': 'delete profile', 'id': profile_id})
            except Exception as e:
                print(f"Error deleting profile: {e}")
        else:
            print("Cancelled.")
    
    def execute_activate(self, profile_id: str) -> None:
        """Activate a profile"""
        if profile_id not in self.profiles:
            print(f"Error: Profile '{profile_id}' not found.")
            return
        
        if self.active_profiles.get(profile_id):
            print(f"Profile {profile_id[:8]}... is already active.")
            return
        
        self.active_profiles[profile_id] = True
        print(f"Profile activated: {profile_id[:8]}...")
        
        if self.request_queue:
            profile = self.profiles[profile_id]
            self.request_queue.put({
                'message': 'add profile',
                'id': profile_id,
                'data': (profile['sender_emails'], profile['receiver_emails'], 
                        profile['password'], profile['topic'], profile['email_content'], 
                        profile['condition'])
            })
    
    def execute_deactivate(self, profile_id: str) -> None:
        """Deactivate a profile"""
        if profile_id not in self.profiles:
            print(f"Error: Profile '{profile_id}' not found.")
            return
        
        if not self.active_profiles.get(profile_id):
            print(f"Profile {profile_id[:8]}... is not active.")
            return
        
        self.active_profiles[profile_id] = False
        print(f"Profile deactivated: {profile_id[:8]}...")
        
        if self.request_queue:
            self.request_queue.put({
                'message': 'deactivate profile',
                'id': profile_id
            })
    
    def execute_duplicate(self, profile_id: str) -> None:
        """Duplicate a profile"""
        if profile_id not in self.profiles:
            print(f"Error: Profile '{profile_id}' not found.")
            return
        
        import copy
        import uuid
        new_id = str(uuid.uuid1())
        new_profile = {new_id: copy.deepcopy(self.profiles[profile_id])}
        self.profiles.update(new_profile)
        self.save_profiles()
        print(f"Profile duplicated: {new_id}")
    
    def execute_export(self, filename: str) -> None:
        """Export profiles to JSON"""
        if not filename:
            filename = "profiles_export.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.profiles, f, indent=2)
            print(f"Profiles exported to {filename}")
        except Exception as e:
            print(f"Error exporting profiles: {e}")
    
    def execute_import(self, filename: str) -> None:
        """Import profiles from JSON"""
        if not filename:
            print("Error: Please provide a filename.")
            return
        
        try:
            with open(filename, 'r') as f:
                imported = json.load(f)
            self.profiles.update(imported)
            self.save_profiles()
            print(f"Imported {len(imported)} profile(s) from {filename}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{filename}'.")
        except Exception as e:
            print(f"Error importing profiles: {e}")
    
    def execute_clear(self) -> None:
        """Clear all profiles"""
        confirm = input("Clear ALL profiles? This cannot be undone (yes/no): ").strip().lower()
        if confirm == "yes":
            self.profiles.clear()
            self.save_profiles()
            print("All profiles cleared.")
        else:
            print("Cancelled.")
    
    def process_command(self, command: str) -> None:
        """Parse and execute commands"""
        parts = command.strip().split(maxsplit=1)
        if not parts:
            return
        
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if cmd == "help":
            self.show_help()
        elif cmd == "list":
            self.list_profiles()
        elif cmd == "view":
            if not arg:
                print("Usage: view <profile_id>")
            else:
                self.view_profile(arg)
        elif cmd == "create":
            self.execute_create()
        elif cmd == "edit":
            if not arg:
                print("Usage: edit <profile_id>")
            else:
                self.execute_edit(arg)
        elif cmd == "delete":
            if not arg:
                print("Usage: delete <profile_id>")
            else:
                self.execute_delete(arg)
        elif cmd == "duplicate":
            if not arg:
                print("Usage: duplicate <profile_id>")
            else:
                self.execute_duplicate(arg)
        elif cmd == "activate":
            if not arg:
                print("Usage: activate <profile_id>")
            else:
                self.execute_activate(arg)
        elif cmd == "deactivate":
            if not arg:
                print("Usage: deactivate <profile_id>")
            else:
                self.execute_deactivate(arg)
        elif cmd == "status":
            self.show_status()
        elif cmd == "export":
            self.execute_export(arg)
        elif cmd == "import":
            if not arg:
                print("Usage: import <filename>")
            else:
                self.execute_import(arg)
        elif cmd == "clear":
            self.execute_clear()
        elif cmd in ("exit", "quit"):
            self.running = False
            print("Goodbye!")
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")
    
    def run(self) -> None:
        """Main command loop - similar to Command Prompt"""
        print("\nEmail Automation Terminal")
        print(f"Profiles: {len(self.profiles)} loaded")
        print(f"Backend: {'Connected' if self.request_queue else 'Standalone'}")
        print("Type 'help' for available commands\n")
        
        while self.running:
            try:
                self.print_header()
                command = input()
                
                if command.strip():
                    self.process_command(command)
                    print()
            except KeyboardInterrupt:
                print("\n\nInterrupted by user")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    # Standalone mode - no backend queues
    tui = EmailAutomationTUI()
    tui.run()
else:
    # Used as module with queues
    pass
