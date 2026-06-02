import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site.settings')
django.setup()

from hive.models import SinglePromptChat, AIVendor

def create_pilot_activity():
    """
    Creates a custom 'Pilot' activity in the OpenMoxie database.
    """
    module_id = "PILOT_SIMULATOR"
    content_id = "default"
    
    prompt = """
    You are Chief Pilot Moxie of the Global Robotics Air Fleet. 
    You are currently in the cockpit of a high-tech experimental jet.
    Your friend is your co-pilot.
    
    Rules:
    1. Respond as a professional but friendly pilot.
    2. Use aviation terminology (e.g., 'Roger', 'Over', 'Copy that', 'Vectoring').
    3. If the user asks about the weather, make up some 'cockpit weather radar' data.
    4. Keep responses under 40 words.
    5. If the user says 'Eject!', respond with '<exit>' to end the simulation.
    
    Current Flight Status: {{session.local_data.altitude|default:"30,000 feet"}} and stable.
    """
    
    opener = "Welcome aboard, co-pilot! Controls are hot. Are you ready for takeoff?|Chief Pilot Moxie reporting for duty. All systems green. What's our flight plan today?"
    
    # Custom Python logic for the activity
    custom_code = """
def pre_process(volley, session):
    # Example: update altitude in local data if user mentions climbing
    if 'climb' in volley.request.get('speech', '').lower():
        alt = session.local_data.get('altitude', 30000)
        session.local_data['altitude'] = alt + 5000
        volley.set_output("Copy that, climbing to " + str(session.local_data['altitude']) + " feet.", None)
        return True # Handled manually
    return False

def complete_handler(volley, session):
    print("Flight simulation completed.")
    """

    # Create or update the activity
    activity, created = SinglePromptChat.objects.update_or_create(
        module_id=module_id,
        content_id=content_id,
        defaults={
            "name": "Moxie Pilot Scenario",
            "prompt": prompt.strip(),
            "opener": opener,
            "max_volleys": 15,
            "vendor": AIVendor.OPEN_AI.value,
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "code": custom_code.strip(),
            "source_version": 1
        }
    )
    
    if created:
        print(f"Created new activity: {activity.name}")
    else:
        print(f"Updated existing activity: {activity.name}")

if __name__ == "__main__":
    create_pilot_activity()
