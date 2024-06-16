Project Structure
plaintext
Copy code
pythonProject7/
├── .git/
├── .idea/
├── venv/
├── Dockerfile
├── crontab
├── main.py
├── README.md
├── requirements.txt
├── trading_log.txt
Dockerfile: Defines the Docker image and environment setup.
crontab: Contains the cron job schedule.
main.py: The main Python script to be executed.
requirements.txt: Lists the Python dependencies.
trading_log.txt: A log file to record trading operations.
Requirements
Docker
Alpaca API credentials (API Key and Secret)
Setup
Clone the repository:

sh
Copy code
git clone https://github.com/ay1ncode/pythonProject7.git
cd pythonProject7
Set your Alpaca API credentials:

Ensure your environment variables for the Alpaca API are set. You can do this by exporting them in your shell or adding them to the Dockerfile.

sh
Copy code
export ALPACA_API_KEY=<Your Alpaca API Key>
export ALPACA_API_SECRET=<Your Alpaca API Secret>
Build the Docker image:

sh
Copy code
docker build -t pythonproject7 .
Running the Application
To run the application, you can start a Docker container using the built image. Ensure no other container is using the name test_alpaca_app.

Running the Container
sh
Copy code
docker run -d --name test_alpaca_app pythonproject7
If the container name test_alpaca_app is already in use, you can either stop and remove the existing container or use a different name.

Stopping and Removing an Existing Container
sh
Copy code
docker stop test_alpaca_app
docker rm test_alpaca_app
Running the Container with a Different Name
sh
Copy code
docker run -d --name new_alpaca_app pythonproject7
Cron Job Schedule
The cron job is set to run the main.py script at 10:00 AM on Mondays and Thursdays. The schedule is defined in the crontab file:

crontab
Copy code
0 10 * * 1,4 root python /app/main.py >> /var/log/cron.log 2>&1
Troubleshooting
If you encounter issues, here are some steps to troubleshoot:

Check Docker Logs:

sh
Copy code
docker logs test_alpaca_app
Inspect the Cron Log:

Inside the container, inspect the /var/log/cron.log file to see the output of the cron jobs.

Ensure Correct Line Endings:

If you are using Windows, ensure the crontab file uses Unix line endings (LF). You can use tools like dos2unix to convert line endings.

Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.
