FROM python:3.8-slim

# Install the dependencies for the PostgreSQL repository
RUN apt-get update && apt-get install -y wget gnupg

# Add the PostgreSQL repository to get the latest PostgreSQL client
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ $(. /etc/os-release; echo $VERSION_CODENAME)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL client version 16
RUN apt-get update && apt-get install -y postgresql-client-16

# Copy the ELT script 
COPY elt_script.py .

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]
