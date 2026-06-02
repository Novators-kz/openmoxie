# Using Moxie with Custom Activities

This guide explains how to use the Moxie robot with custom activities in code, using a "Pilot" scenario as an example.

## Core Concepts

In OpenMoxie, an activity is a **Module**. Each module has a **Module ID** and a **Content ID**. Remote activities are backed by the [SinglePromptChat](./site/hive/models.py#9-26) model in the database.

## Step 1: Register the Activity
Run the example script to add the Pilot activity to your local database:
```bash
python local/examples/pilot_activity.py
```
This script creates a [SinglePromptChat](./site/hive/models.py#9-26) record with a custom system prompt and Python hooks.

## Step 2: Choose a Launch Method

There are three primary ways to actually *start* this activity on your Moxie robot:

### Method A: Global Voice Command (Easiest)
You can create a "Global Response" that triggers the activity when you say a specific phrase.
1. Run the trigger script:
   ```bash
   python local/examples/trigger_activity.py
   ```
2. Now, whenever you say **"Start the pilot simulator"**, Moxie will respond with a confirmation and switch to the Pilot activity.

### Method B: AI Transition (In-Conversation)
You can tell one AI persona to "hand off" the conversation to the Pilot.  
In any other module's **prompt** or **code**, include the launch tag:
```xml
I think you should talk to my friend at the airport. <launch:PILOT_SIMULATOR:default>
```
When the AI outputs this tag, the [RemoteChat](./site/hive/mqtt/moxie_remote_chat.py#37-206) engine automatically intercepts it and switches modules.

### Method C: Adding to the Schedule
If you want the activity to appear naturally during Moxie's day:
1. Open the Django Admin (if running) or use a script to modify a [MoxieSchedule](./site/hive/models.py#27-34).
2. Add an entry to the [schedule](./site/hive/mqtt/scheduler.py#78-113) JSON field:
   ```json
   { "module_id": "PILOT_SIMULATOR", "content_id": "default" }
   ```

## Step 3: Interaction Logic

Once active, the Pilot scenario uses:
- **State Awareness**: Keeps track of `altitude` in `session.local_data`.
- **Python Hooks**: The `pre_process` function in [pilot_activity.py](./local/examples/pilot_activity.py) handles specific commands like "climb".
- **Exit Logic**: Saying "Eject!" triggers the `<exit>` tag which returns Moxie to its previous state/schedule.

## Summary of Files
- [pilot_activity.py](./local/examples/pilot_activity.py) - Register the activity.
- [trigger_activity.py](./local/examples/trigger_activity.py) - Create a voice trigger.
