import argparse
import json
import signal
import sys


contacts_file_name: str = ""
contacts: dict[str, str] = {}


def handle_system_signal(sig, frame) -> None:
    _, _ = sig, frame
    print("\nTermination signal received. Shutting down...")
    shutdown()


def validate_contacts() -> None:
    if len(contacts) == 0:
        return

    if not isinstance(contacts, dict):
        raise ValueError(f"structure of {contacts_file_name} is not a "
                         "dictionary")

    for name, phone in contacts.items():
        if not isinstance(name, str):
            raise ValueError(f"in {contacts_file_name} name {name} is not a "
                             f"string, but {type(name)}")
        if not isinstance(phone, str):
            raise ValueError(f"in {contacts_file_name} at name {name} phone "
                             f"{phone} is not a string, but {type(phone)}")


def load_contacts() -> None:
    if not contacts_file_name:
        raise ValueError("file name is not specified (empty)")

    if not contacts_file_name.endswith(".json"):
        raise ValueError(f"file {contacts_file_name} is not a JSON file")

    global contacts
    with open(contacts_file_name, "a+") as fh:
        fh.seek(0)
        contacts = json.load(fh)

    validate_contacts()


def save_contacts() -> None:
    if not contacts_file_name:
        raise ValueError("file name was not specified (empty)")

    if len(contacts) == 0:
        return

    with open(contacts_file_name, "w") as fh:
        json.dump(contacts, fh, indent=4)


def greet() -> str:
    return "How can I help you?"


def add_contact(name: str, phone: str) -> str:
    if name in contacts:
        return f"Name {name} already exists. Use command \"change\" to update"

    contacts[name] = phone
    return f"{name} was added to your contacts"


def change_contact(name: str, phone: str) -> str:
    if name not in contacts:
        return f"There is no {name} in contacts. Use command \"add\" to create"

    contacts[name] = phone
    return f"{name}'s contact was updated"


def show_phone(name: str) -> str:
    if name not in contacts:
        return f"There is no {name} in contacts. Use command \"add\" to create"

    return contacts[name]


def get_all() -> str:
    if len(contacts) == 0:
        return "You have no saved contacts yet"

    contacts_to_return = ""

    for name, phone in contacts.items():
        contacts_to_return += name + " " + phone + "\n"

    return contacts_to_return.rstrip()


def shutdown():
    try:
        save_contacts()
    except Exception as e:
        print(f"Unable to save contacts: {e}")
    finally:
        sys.exit(0)


def init():
    signal.signal(signal.SIGINT, handle_system_signal)
    signal.signal(signal.SIGTERM, handle_system_signal)

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str,
                        help="Path to the json file with saved contacts",
                        default="./data/contacts.json")

    args = parser.parse_args()

    global contacts_file_name
    contacts_file_name = args.file

    try:
        load_contacts()
    except Exception as e:
        print(f"Unable to load contacts file: {e}")
        sys.exit(0)


def handle_command(command: dict[str, str]) -> str:
    cmd = command["command"]

    if cmd == "hello":
        return greet()
    if cmd == "add":
        return add_contact(command["name"], command["phone"])
    if cmd == "change":
        return change_contact(command["name"], command["phone"])
    if cmd == "phone":
        return show_phone(command["name"])
    if cmd == "all":
        return get_all()

    return f"Invalid command: {cmd}"


def parse_command(user_input: str) -> dict[str, str]:
    user_input = user_input.strip()

    if user_input == "":
        return {}

    command_components = user_input.split()
    command = command_components[0].lower()
    name = ""
    phone = ""

    if len(command_components) > 1:
        name = command_components[1]

    if len(command_components) > 2:
        phone = command_components[2]

    return {"command": command, "name": name, "phone": phone}


def main():
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("console bot >>> ")
        command = parse_command(user_input)
        if command is None:
            print("No command was entered. Try again")
        elif command["command"] in ("exit", "q", "quit", "close", "good bye"):
            break
        message = handle_command(command)
        if message:
            print(message)

    print("Good bye!")
    shutdown()


if __name__ == "__main__":
    init()
    main()
