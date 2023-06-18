#!/bin/bash

# Retrieve RDS environment variables
RDS_INFO=$(/opt/elasticbeanstalk/bin/get-config addons -a rds)
HOST=$(echo "$RDS_INFO" | jq -r '.env.RDS_HOSTNAME')
PORT=$(echo "$RDS_INFO" | jq -r '.env.RDS_PORT')
DB_NAME=$(echo "$RDS_INFO" | jq -r '.env.RDS_DB_NAME')
USERNAME=$(echo "$RDS_INFO" | jq -r '.env.RDS_USERNAME')
PASSWORD=$(echo "$RDS_INFO" | jq -r '.env.RDS_PASSWORD')

echo "Seeding RDS database...\n"
# Path to your SQL file
SQL_FILE="./init.sql"

# Connect to the database and execute SQL file
mysql -h "$HOST" -P "$PORT" -u "$USERNAME" -p"$PASSWORD" "$DB_NAME" < "$SQL_FILE"

# Check the exit code of the previous command
if [ $? -ne 0 ]; then
  echo "Error executing MySQL statement. Exiting..."
  exit 1
fi

echo "Completed seeding RDS database"

exit 0
