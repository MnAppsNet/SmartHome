#!/bin/bash
serviceName="smartThermostat.service"
startScript="${PWD}/service.sh"
serviceFile="/etc/systemd/system/${serviceName}"

touch "$startScript"
sudo chmod +x "$startScript"
echo '''#!/bin/bash
cd server
python3 smartThermostat.py''' > "$startScript"
sudo sh -c "cat > $serviceFile <<- EOM
[Unit]
Description=SmartThermostat
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=5
User=${USER}
WorkingDirectory=${PWD}
ExecStart=${startScript}

[Install]
WantedBy=multi-user.target
EOM"
sudo systemctl daemon-reload
sudo systemctl enable ${serviceName}
sudo systemctl start ${serviceName}
echo "${serviceName} is ready..."