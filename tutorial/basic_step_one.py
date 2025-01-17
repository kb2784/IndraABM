"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

import lib.actions as acts
import lib.model as mdl


MODEL_NAME = "segregation"

NUM_RED = 250
NUM_BLUE = 250


def env_action(agent, **kwargs):
    """
    Just to see if this works!
    """
    print("The environment does NOT look perilous: you can relax.")


def basic_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    if acts.DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name,
                                                 agent.get_pos()))
    for neighbor in acts.get_neighbors(agent):
        print(f"{str(agent)} has neighbor {str(neighbor)}")
    return acts.MOVE


segregation_grps = {
    "blue_group": {
        mdl.MBR_ACTION: basic_action,
        mdl.NUM_MBRS: NUM_BLUE,
        mdl.NUM_MBRS_PROP: "num_blue",
        mdl.COLOR: acts.BLUE
    },
    "red_group": {
        mdl.MBR_ACTION: basic_action,
        mdl.NUM_MBRS: NUM_RED,
        mdl.NUM_MBRS_PROP: "num_red",
        mdl.COLOR: acts.RED
    },
}


class Segregation(mdl.Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return Segregation(serial_obj=serial_obj)
    else:
        return Segregation(MODEL_NAME,
                           grp_struct=segregation_grps,
                           props=props,
                           env_action=env_action,
                           create_for_test=create_for_test,
                           exec_key=exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
