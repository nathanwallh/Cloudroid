echo 233 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio233/direction
echo 1 > /sys/class/gpio/gpio233/value
