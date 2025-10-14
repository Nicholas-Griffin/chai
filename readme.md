# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name: Nicholas Griffin**

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.


1. What are two different designs you contemplated for your multiple conversations implementation?

At first I contemplated having each conversation have 3 variables. One with the userID, one with a list of user prompts, and one with a list of the AI responses
Then I swapped to my current system which is much better. one Json with a list of conversations and the UserIDs corresponding, and one for each conversation.

2. A vibe coder wants to make a quick MVP (minimum viable product) over the weekend that handles chat threads with AI models. Do you recommend using JSON files for persistence? Why?
I don't. Jsons are the bain of my existence and it takes way longer than a weekned to understand.

3. You are interviewing at OpenAI. The interviewer asks if you would use raw JSON files to store user chats or if you would use a database or other form of persistence and to explain your choice. How would you reply?
I would use a database. Databases are much more uniform and easier for humans to make sense of in debugging and the like. As long as formatted properely, both humans and computers can easily understand it.

4. What did you notice about performance using this file storage method?
I noticed it often takes 0.02-0.04 seconds to work each action. On larger scales it would take longer and longer. Not to mention that we haven't even tackled the AI responses yet.
