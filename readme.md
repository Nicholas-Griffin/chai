# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** Nicholas Griffin

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.

## Lab 2: MongoDB Integration & Performance Analysis

Question 1: Performance Analysis (5P)

Run Performance.py and record the reulsts. What did you observe about:

    How append times changed as the number of messages grew for flat files vs MongoDB?

        FFs started much faster at 10 messages but got slower at 100 (0.29ms -> 0.62ms)

        MDB started slower but sped up, primarily because of the start up time of MDB (1.22ms -> 0.67ms)

    The difference in read times for retrieving the full conversation?

        FFs read 100 messages in 0.13ms

        MDB reads 100 messages in 0.55ms

Explain WHY you see these performance characteristics.

    The primary reason FFs are faster in these scenarios is because FFs access the files directly, because the files would be in the same directory. Meanwhile, Mongo has to start up and connect before doing anything, and even then has to access a database in a completely differenct location.

    If the samples were larger (1000+ messages), MongoDB would be similar in speed, or even better than, FFs. 

Question 2: Atomic Operations (5P)

    In MongoDBManager, we use the $push operator in append_message(). 
    Research what "atomic operations" means in the context of databases. 

    Why is this important for a chat application where multiple messages might be added rapidly?

        Atomic Operations are simply operations that follow the rule of Atomicity in ACID (All or None).

        Atomicity is important for a variety of reasons, but most importantly, it ensures the data is properely stored. For example, if I had two seperate append functions, one for the user and one for the bot, on the chance that one of the functions failed it simply wouldn't save those messages, leaving huge gaps in your data and making it impossible to recall what was said the last time you were in the thread


Question 3: Scalability (5 points)

Imagine your chat application goes viral and now has 1 million users, each with an average of 10 conversation threads containing 500 messages each.

Compare how FlatFileManager and MongoDBManager would handle:

    Finding all threads for a specific user

        FFM would find all threads of a user by slowly iterating through all threads with the specific user_id.

        Meanwhile with MDBM all you have to do is run the list_user_threads function, which simply uses "find" with a few specific parameters

    Loading a specific conversation

        With FFM, you use "get_conversation(FFM, conversation_ID)" and print ot out

        with MDBM, you use the same function but with MDBM, userID, and threadName

        The big difference is that MDBM uses "find_one" while FFM doesn't have such a feature, because of this MDBM has 4 lines for "get_conversation" while FFM has 9, more than double.

        Needless to say, this would make a huge difference in bigger projects

    Storage organization and file system limits

        FFM stores data in JSONS found directly in the chai folder, called "conversations.json".
        If I remember right, FFM stores user_ids and conversation_ids in conversations.json and then has a JSON for each conversation.
        It's not very scalable, and it can get hard to use in bigger datasets, also not very space effecient for nig projects.

        Meanwhile, MDBM stores data in BSONS which are in the MongoDB Database connected.
        MDBM stores one conversation_id and an embedded array of messages.
        While it's much more efficient and scalable than FFM, you can't manually manage files, you have to go through Mongo.
        

Question 4: Data Modeling Design Challenge (5 points)

Currently, each conversation is stored as a single document with an embedded array of messages:

    {
    "_id": "user_123_work",
    "messages": [...]
    }

An alternative design would be to store each message as its own document:

    {
    "_id": "msg_001",
    "conversation_id": "user_123_work",
    "role": "user",
    "content": "Hello!",
    "timestamp": "..."
    }

Describe:

    One advantage of the embedded messages design (what we currently use)

        An advantage of embedded messages is not needing to get each and every message individually. You run one "find_one" command and you have the entire history.

    One advantage of the separate message documents design

        An advantage of seperate messages is the ability to access messages individually based on context or time. You could, for example, only access the five most recent messages when starting up the chat, saving time and bandwidth.

    A scenario where you would choose the separate messages design instead

        One scenario where I would choose to use seperate messages is in a situation where I don't have a storage constraint and want as much documentation per message as possible: Timestamps. Or when I want to be able to look for a message with specific words without opening the entire chat. 
        EX: (
            find(
                {"conversation_id": conversation_id}, 
                    {
                    "_id": True, 

                    "role": False, 
                    
                    [I dont know Python syntax for this but it would be similar to contains(ignoreCase("Custom Message"))]
                    }
                )
            )

(This is a real design decision MongoDB developers face. There's no single "right" answer because it depends on your access patterns and scale.)
