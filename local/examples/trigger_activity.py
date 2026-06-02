import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site.settings')
django.setup()

from hive.models import GlobalResponse, GlobalAction

def create_trigger():
    """
    Creates a GlobalResponse that triggers the Pilot activity
    when the user says a specific phrase.
    """
    name = "Trigger Pilot Simulator"
    pattern = r"^(start|begin|open) (the )?pilot simulator$"
    module_id = "PILOT_SIMULATOR"
    content_id = "default"
    response_text = "Roger that! Initializing cockpit systems. Please stand by for takeoff."
    
    # Create or update the global response
    trigger, created = GlobalResponse.objects.update_or_create(
        name=name,
        defaults={
            "pattern": pattern,
            "action": GlobalAction.LAUNCH.value,
            "module_id": module_id,
            "content_id": content_id,
            "response_text": response_text,
            "sort_key": 100 # High priority
        }
    )
    
    if created:
        print(f"Created new trigger: {trigger.name}")
    else:
        print(f"Updated existing trigger: {trigger.name}")

if __name__ == "__main__":
    create_trigger()
