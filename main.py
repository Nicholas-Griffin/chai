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

    conversation_id = getConversationId(db_manager)

    run_chat(db_manager, conversation_id)

def getConversationId(db_manager: FlatFileManager) -> str:
    existingConversations = list(db_manager.conversations_index.keys())

    if existingConversations:
        print("Existing Conversations:\n")
        for i, convo in enumerate(existingConversations, start=1):
            print(f"{i} {convo}")
        print("\nPlease choose which conversation to continue via numbers (1, 7, 69, 420, etc). \nTo create a new conversation type the title of the new conversation.")
    else:
        print("No Previous Conversations. \n\nTo create a new conversation type the title of the new conversation.")
        
    user_input = input("> ")

    if user_input.isdigit() and 1<= int(user_input) and int(user_input) <= len(existingConversations):
        conversation_id = existingConversations[int(user_input) - 1]
        return conversation_id
    
    if user_input.isdigit():
        print("\nIf you are trying to make a new conversation, please refrain from starting with digits.")
        print("Otherwise, the conversation doesn't exist.")
        print("Please try again \n\n")
        return getConversationId(db_manager)
    
    conversation_id = f"{user_input}_conversation"
    return conversation_id

def run_chat(db_manager: FlatFileManager, conversation_id: str) -> None:
    start_time = time.time()
    messages = db_manager.get_conversation(conversation_id)
    end_time = time.time()
    duration = end_time - start_time

    if messages:
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")
        print(f"Load time: {duration:.4f} seconds")

    print(f"Conversation: {conversation_id}. Type 'exit' to quit.")

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