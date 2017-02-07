FROM mavros_optitrack
MAINTAINER Jerome Guzzi "jerome@idsia.ch"


COPY . /home/root/catkin_ws/src/mavros_merger
RUN /bin/bash -c '. /opt/ros/kinetic/setup.bash; catkin_make -C /home/root/catkin_ws;'
