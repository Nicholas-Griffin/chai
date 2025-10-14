import os
import json
import shutil
from typing import List


class FlatFileManager:
    """
    Manages storing and retrieving chat conversations in flat JSON files.
    """
    def __init__(self, storage_dir="data"):
        """
        Initializes the FlatFileManager for a specific user.

        Args:
            storage_dir (str): The unique identifier for the user.
        """
        self.storage_dir = storage_dir
        self._ensure_storage_exists()

        self.conversations_index = {} # Key: conversation_id => Value: Filepath
        self.users_index = {}

        self._init_conversation_index()
        self._init_user_index()

    #             INITS

    def _ensure_storage_exists(self) -> None:

        os.makedirs(self.storage_dir, exist_ok=True)
        print(f"Storage Directory '{self.storage_dir}' is ready.")

    def _init_conversation_index(self) -> None:

        index_file = os.path.join(self.storage_dir, "conversations.json")
        if not os.path.exists(index_file):
            self.save_index()
        with open(index_file, "r") as f:
            self.conversations_index = json.load(f)

    def _init_user_index(self) -> None:

        index_file = os.path.join(self.storage_dir, "users.json")
        if not os.path.exists(index_file):
            self.save_user_index()
        with open(index_file, "r") as f:
            self.users_index = json.load(f)

    #             SAVES

    def save_index(self) -> None:

        index_file = os.path.join(self.storage_dir, "conversations.json")
        with open(index_file, "w") as f:
            json.dump(self.conversations_index, f, indent=3)

    def save_user_index(self) -> None:

        index_file = os.path.join(self.storage_dir, "users.json")
        with open(index_file, "w") as f:
            json.dump(self.users_index, f, indent=3)

    #             USERS

    def get_user_conversations(self, user_id: str) -> List[str]:
        return self.users_index.get(user_id, [])

    def add_conversation_to_user(self, user_id: str, conversation_id: str) -> None:
        if user_id not in self.users_index:
            self.users_index[user_id] = []
        if conversation_id not in self.users_index[user_id]:
            self.users_index[user_id].append(conversation_id)
            self.save_user_index

    #             CONVO

    def get_conversation(self, conversation_id: str) -> List[any]:

        conversation = self.conversations_index.get(conversation_id)
        if not conversation:
            return []
        conversation = os.path.join(self.storage_dir,conversation)
        try:
            with open(conversation, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return []

    def save_conversation(self, conversation_id: str, relative_filepath: str, messages: List[any]) -> None:

        #Asked ChatGPT why I was failing to save conversation and it said to convert the relative filepath to a full path
        full_path = os.path.join(self.storage_dir, relative_filepath)
        
        with open(full_path, "w") as f:
            json.dump(messages, f, indent=3)
        
        self.conversations_index.update({conversation_id: relative_filepath})
        self.save_index()

    def run_tests(self):
        print("Testing FlatFileManager._ensure_storage_exists()")
        # manually check that file exists
        if not os.path.isdir(self.storage_dir):
            print("Failed to create directory!")
            return

        print("Testing FlatFileManager.save_conversation()")
        messages = [{"role": "user", "content": "hello world"}]
        conversation_id = "test_user"
        relative_filepath = "test_user.json"

        self.save_conversation(conversation_id, relative_filepath, messages)
        filepath = os.path.join(manager.storage_dir, relative_filepath)
        if not os.path.exists(filepath):
            print("Failed to save conversation!")
            return
        print("Successfully saved conversation!")

        print("Testing FlatFileManager.get_conversation()")
        read_messages = self.get_conversation(conversation_id)
        if not read_messages:
            print("Failed to get conversation!")
            return
        print("Successfully retrieved conversation!")

        try:
            shutil.rmtree(self.storage_dir)
            print("Deleted storage directory")
        except OSError as e:
            print(f"Failed to delete storage directory: {e}")

        print("All tests passed!")



if __name__ == "__main__":
    print("Testing FlatFileManager")
    manager = FlatFileManager(storage_dir="data_test")
    manager.run_tests()