#!/usr/bin/env python
from __future__ import print_function
import rospy
from mavros_msgs.msg import Mavlink
from mavros_merger.msg import ConnectionArray
from std_msgs.msg import Header


class Merger(object):
    """docstring for PathFollower"""

    def __init__(self):
        super(Merger, self).__init__()
        rospy.init_node('mavros_merger', anonymous=False)
        controllers = rospy.get_param("~controllers", [])
        drones = rospy.get_param("~drones", {})
        self.pubs = {}
        self.conn_pubs = {}
        self.connections = {}
        rospy.loginfo("%s %s", drones, controllers)

        for c in controllers:
            c_uri = "{c}/connections".format(**locals())
            self.connections[c] = ({}, rospy.Publisher(c_uri, ConnectionArray,
                                                       queue_size=1))

        for uid, ns in drones.items():
            s_uri = "{uid}/mavlink/from".format(**locals())
            d_uri = "{ns}/mavlink/from".format(**locals())
            self.pubs[uid] = [None,
                              rospy.Publisher(d_uri, Mavlink, queue_size=5)]
            for c in controllers:
                uri = "{c}/{s_uri}".format(**locals())
                rospy.Subscriber(uri, Mavlink,
                                 self.has_received_mavlink(c, uid, ns))
        rospy.Timer(rospy.Duration(1), self.pub_connections, oneshot=False)
        rospy.spin()

    def pub_connections(self, evt):
        for _, (cs, pub) in self.connections.items():
            n = rospy.Time.now()
            nss = [ns for (ns, ts) in cs.items() if (n - ts).to_sec() < 1]
            pub.publish(header=Header(stamp=rospy.Time.now()), connections=nss)

    def has_received_mavlink(self, c, uid, ns):
        pub = self.pubs[uid]
        connections = self.connections[c][0]

        def cb(msg):
            rospy.logdebug("c {c}\t"
                           "seq {msg.seq:03d}\t"
                           "status {msg.framing_status:d}\t"
                           "checksum {msg.checksum:05d}\t"
                           "timestamp {msg.header.stamp}".format(c=c, msg=msg))

            # Is valid
            if msg.framing_status == Mavlink.FRAMING_OK:
                if pub[0] is None or (msg.seq - pub[0] + 254) % 255 < 128:
                    pub[0] = msg.seq
                    pub[1].publish(msg)
                    rospy.logdebug("-> publish from %s", c)
                connections[ns] = rospy.Time.now()
        return cb


if __name__ == '__main__':
    Merger()
