import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hemolyze.settings')
django.setup()

from django.db import connection

def fix_database():
    print("Starting database cleanup...", flush=True)
    
    # First, delete all records from ReceivedBlood table to avoid foreign key constraint issues
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM blood_request_receivedblood
        """)
        received_blood_count = cursor.rowcount
        print(f"Deleted {received_blood_count} records from ReceivedBlood table", flush=True)
    
    # Then, delete invalid AcceptBloodRequest records that reference non-existent BloodRequests
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM blood_request_acceptbloodrequest 
            WHERE request_user_id NOT IN (SELECT id FROM blood_request_bloodrequest)
        """)
        invalid_request_count = cursor.rowcount
        print(f"Deleted {invalid_request_count} invalid AcceptBloodRequest records", flush=True)
    
    print("Database cleanup completed successfully!", flush=True)

if __name__ == "__main__":
    try:
        fix_database()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        sys.exit(1)