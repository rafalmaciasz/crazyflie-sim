"""Example connection with CrazyFlie."""

import logging
import sys
import time
from threading import Event
from typing import Any, Dict

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
CF_URI = uri_helper.uri_from_env(default="udp://0.0.0.0:19850")

DEFAULT_HEIGHT = 1

deck_attached_event = Event()

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


def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.turn_left(180)
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)


if __name__ == "__main__":
    cflib.crtp.init_drivers(enable_debug_driver=False)

    lg_stab = LogConfig(name="Stabilizer", period_in_ms=10)
    lg_stab.add_variable("motor.m1", "uint16_t")
    lg_stab.add_variable("motor.m2", "uint16_t")
    lg_stab.add_variable("motor.m3", "uint16_t")
    lg_stab.add_variable("motor.m4", "uint16_t")

    with SyncCrazyflie(CF_URI, cf=Crazyflie(rw_cache="./cache")) as scf:
        scf.cf.platform.send_arming_request(True)
        simple_log_async(scf, lg_stab)

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)
        
        # if not deck_attached_event.wait(timeout=5):
        #     print('No flow deck detected!')
        #     sys.exit(1)

        take_off_simple(scf)

        print("Disconnecting...")
    print("Disconnected.")
