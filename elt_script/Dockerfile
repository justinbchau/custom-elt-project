FROM python:3.8-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client cron

# Copy the wrapper script and the ELT script
COPY start.sh /app/start.sh
COPY elt_script.py .

# Set the working directory
WORKDIR /app

# Add the cron job
# This example runs the script every day at 3am.
# Adjust the cron timing as needed.
RUN echo "0 3 * * * python /app/elt_script.py" | crontab -


# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]