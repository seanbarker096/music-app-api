#!/bin/bash

# Retrieve RDS environment variables
HOST="$RDS_HOSTNAME"
PORT="$RDS_PORT"
DB_NAME="$RDS_DB_NAME"
USERNAME="$RDS_USERNAME"
PASSWORD="$RDS_PASSWORD"

echo "Seeding RDS database...\n"
# Path to your SQL file
SQL_FILE="./schema.sql"

# Connect to the database and execute SQL file
mysql -h "$HOST" -P "$PORT" -u "$USERNAME" -p"$PASSWORD" "$DB_NAME" < "$SQL_FILE"

# Check the exit code of the previous command
if [ $? -ne 0 ]; then
  echo "Error executing MySQL statement. Exiting..."
  exit 1
fi

echo "Completed seeding RDS database"

exit 0
