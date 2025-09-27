sudo systemctl stop gcsv2
cp main /home/datam/azadi-gate/dist/main
sudo systemctl daemon-reload
sudo systemctl start gcsv2
