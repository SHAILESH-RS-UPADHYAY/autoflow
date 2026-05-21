import schedule
import time
from datetime import datetime
from generator import generate_report

def job():
    print(f"\n--- [AutoFlow Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ---")
    try:
        report = generate_report()
        
        # Save to markdown file (in production, this could email to executives)
        filename = f"weekly_report_{datetime.now().strftime('%Y_%m_%d')}.md"
        with open(filename, "w") as f:
            f.write(report)
            
        print(f"Report generated successfully and saved to {filename}!")
    except Exception as e:
        print(f"Error during AutoFlow execution: {e}")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    print("AutoFlow Scheduler Started.")
    print("Pipeline will run every Monday at 08:00 AM.")
    
    # Run once immediately for testing purposes
    print("Running an initial test job...")
    job()
    
    # Schedule for every Monday at 8 AM
    schedule.every().monday.at("08:00").do(job)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)
