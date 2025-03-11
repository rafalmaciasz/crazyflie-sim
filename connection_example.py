"""Example connection with CrazyFlie."""

import logging
import time
from typing import Any, Dict

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
CF_URI = uri_helper.uri_from_env(default="udp://0.0.0.0:19850")

# Set up logging
logging.basicConfig(level=logging.ERROR)


def _log_stab_clb(timestamp: int, data: Dict[str, Any], logconf: LogConfig):
    print(f"[{timestamp}][{logconf.name}]: {data}")


def simple_log_async(scf: SyncCrazyflie, logconf: LogConfig):
    """Log some data from the Crazyflie."""
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(_log_stab_clb)
    logconf.start()


if __name__ == "__main__":
    cflib.crtp.init_drivers(enable_debug_driver=False)

    lg_stab = LogConfig(name="Stabilizer", period_in_ms=10)
    lg_stab.add_variable("stabilizer.roll", "float")
    lg_stab.add_variable("stabilizer.pitch", "float")
    lg_stab.add_variable("stabilizer.yaw", "float")

    with SyncCrazyflie(CF_URI, cf=Crazyflie(rw_cache="./cache")) as scf:
        simple_log_async(scf, lg_stab)

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        print("Disconnecting...")
    print("Disconnected.")
