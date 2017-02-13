FROM mavros:mocap
MAINTAINER Jerome Guzzi "jerome@idsia.ch"

COPY . src/mavros_merger
RUN catkin build
