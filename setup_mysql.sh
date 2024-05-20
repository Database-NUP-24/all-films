#!/bin/bash

# Update the package list
sudo apt-get update

# Install MySQL server
sudo apt-get install -y mysql-server

# Start MySQL service
sudo service mysql start

# Secure MySQL installation (this will require manual input)
sudo mysql_secure_installation

# Create a new database and user (you can modify these variables)
DB_NAME="films_db"
DB_USER="film_user"
DB_PASS="film_password"

# Log in to MySQL as root and execute the commands to set up the database and user
sudo mysql -u root <<MYSQL_SCRIPT
CREATE DATABASE ${DB_NAME};
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# Output the MySQL database and user details
echo "MySQL database and user created."
echo "Database: ${DB_NAME}"
echo "User: ${DB_USER}"
echo "Password: ${DB_PASS}"
