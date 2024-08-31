# import schedule
# import time

# def job():
#     print("Job is running")

# # Schedule the job and keep a reference to it
# scheduled_job = schedule.every().day.at("11:59").do(job)

# # Cancel the job forever after 5 seconds
# time.sleep(5)
# schedule.cancel_job(scheduled_job)
# print("Job has been canceled forever")

# # Keep the script running to show that the job no longer runs
# while True:
#     schedule.run_pending()
#     time.sleep(1)