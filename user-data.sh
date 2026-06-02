#!/bin/bash
set -e

# Update system
apt-get update -y
apt-get upgrade -y

# Install dependencies
apt-get install -y nginx python3 python3-pip awscli

# Variables (CHANGE THIS)
S3_URI="s3://website-storage-devops-demo-201841003492-us-east-1-an/everybody-poops"
APP_DIR="/opt/app"

# Pull repo from S3
rm -rf $APP_DIR
mkdir -p $APP_DIR
aws s3 sync $S3_URI $APP_DIR

cd $APP_DIR

# Install Python dependencies if needed
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
fi

# Create systemd service for the Python app
cat > /etc/systemd/system/app.service <<EOF
[Unit]
Description=Everybody Poops App
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 main.py
Restart=always
StandardOutput=append:/var/log/app.log
StandardError=append:/var/log/app.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable app
systemctl start app

# Configure nginx to listen on port 80 and proxy to 8000
cat > /etc/nginx/sites-available/app <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable site
rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/

# Restart nginx
systemctl enable nginx
systemctl restart nginx