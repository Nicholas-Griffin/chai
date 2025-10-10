import time
import os
from db_wrappers.flat_file_manager import FlatFileManager

def main():
    """
    Main function to run the Chai AI chat application.
    Handles the REPL (Read-Eval-Print Loop) for user interaction.
    """
    print("Welcome to Chai!")
    user_id = input("Please enter your user ID to begin: ")

    db_manager = FlatFileManager("data")

    # --- TODO 6 (do this last): Create a way for a user_id to have multiple conversation threads
    # Requirements:
    #   - If user already exists, then have the user select which thread (conversation_id) they want to use
    #       - Give the option to use a new thread
    #   - Proceed to run_chat() with the correct conversation_id
    #   Hint: This is not a "clean" addition, you may need to restructure how data is stored and indexed
    #         There are many ways to do this. Devise a plan and implement your own solution.

    conversation_id = f"{user_id}_conversation"
    run_chat(db_manager, conversation_id)

def run_chat(db_manager: FlatFileManager, conversation_id: str) -> None:
    start_time = time.time()
    messages = db_manager.get_conversation(conversation_id)
    end_time = time.time()
    duration = end_time - start_time
    if messages:
        for message in messages:
            print(message)
        print(f"Load time: {duration:.4f} seconds")

    print(f"Conversation: '{conversation_id}'. Type 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        start_time = time.perf_counter()

        if not messages:
            messages = db_manager.get_conversation(conversation_id)

        messages.append({"role": "user", "content": user_input})

        ai_response = "This is a mock response from the AI."
        messages.append({"role": "assistant", "content": ai_response})

        relative_filepath = f"{conversation_id}.json"
        db_manager.save_conversation(conversation_id, relative_filepath, messages)

        # ----------------------------------------------------

        end_time = time.perf_counter()
        duration = end_time - start_time

        # ---------------------------------------------------

        print(f"AI: {ai_response}")
        print(f"(Operation took {duration:.4f} seconds)")


if __name__ == "__main__":
    main()