echo 233 > /sys/class/gpio/export
echo out > /sys/class/gpio/export/gpio233/direction
echo 1 > /sys/class/gpio/export/gpio233/value
