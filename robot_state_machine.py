"""

"""
from statemachine import State
from statemachine import StateMachine

from robot_model import RobotModel
from statemachine.contrib.diagram import DotGraphMachine


class RobotStateTransition(StateMachine, RobotModel):
    """ STATES """
    start = State(initial=True)         # Turning on robot
    idle = State()                      # Robot on magnetic line, ready to receive command
    lost = State()                      # Robot has lost magnetic line
    remote_control = State()            # Remote control
    getting_package = State()           # Execute mission - going after package
    loading_package = State()           # Execute mission - waiting for package loaded
    deliver_package = State()           # Execute mission - deliver package
    unloading_package = State()         # Execute mission - waiting for package to be unloaded
    approach_charger = State()          # Execute mission - drive to charger
    charge = State()                    # Robot is at charging position
    deapproach_charger = State()        # Execute mission - drive away from charger
    obstacle = State()                  # Obstacle detected during mission
    error = State()                     # Error state - any error (BLDC lost, lidar lost, ...)
    end = State(final=True)             # Shutting down robot

    """ TRANSITION """
    turn_on = start.to(idle)

    lost_line = idle.to(lost)
    go_charging = idle.to(approach_charger) | charge.to.itself()
    get_package = idle.to(getting_package)
    charger_detected = idle.to(charge)

    found_line = lost.to(idle)

    plan_executed = getting_package.to(loading_package) | deliver_package.to(unloading_package)
    loaded = loading_package.to(deliver_package)
    unloaded = unloading_package.to(idle)

    is_obstacle = getting_package.to(obstacle) | deliver_package.to(obstacle) | \
                  approach_charger.to(obstacle) | deapproach_charger.to(obstacle)
    no_obstacle = obstacle.to(getting_package, cond=['no_obstacle_cond']) | \
                  obstacle.to(deliver_package, cond=['no_obstacle_cond']) | \
                  obstacle.to(approach_charger, cond=['no_obstacle_cond']) | \
                  obstacle.to(deapproach_charger, cond=['no_obstacle_cond'])

    charger_reached = approach_charger.to(charge)
    retreat_charging = charge.to(deapproach_charger)

    human_control_on = idle.to(remote_control) | lost.to(remote_control) | \
                       charge.to(remote_control) | error.to(remote_control)
    human_control_off = remote_control.to(idle)

    is_error = idle.to(error) | lost.to(error) | charge.to(error)
    no_error = error.to(idle)

    # Task in canceled by server or failed by robot
    cancel_task = approach_charger.to(idle) | deapproach_charger.to(idle) | \
                  getting_package.to(idle) | loading_package.to(idle) | \
                  deliver_package.to(idle) | unloading_package.to(idle) | \
                  obstacle.to(idle)

    turn_off = idle.to(end) | lost.to(end) | charge.to(end)| error.to(end)

    """ SELF TRANSITION (not used yet)"""
    # internal_start = start.to.itself(internal=True, on='on_idle')
    # internal_idle = idle.to.itself(internal=True, on='on_idle')
    # internal_idle_lost = idle_lost.to.itself(internal=True, on='on_idle')
    # internal_remote_control = remote_control.to.itself(internal=True, on='on_idle')
    # internal_waypoint_follower = waypoint_follower.to.itself(internal=True, on='on_idle')
    # internal_approach_charger = approach_charger.to.itself(internal=True, on='on_idle')
    # internal_at_charger = at_charger.to.itself(internal=True, on='on_idle')
    # internal_deapproach_charger = deapproach_charger.to.itself(internal=True, on='on_idle')
    # internal_error = error.to.itself(internal=True, on='on_idle')
    # st = start.to(start)

    def __init__(self, robot_name='robot_'):
        StateMachine.__init__(self)
        RobotModel.__init__(self, robot_name)

        self.last_state = None

        print(f'Robot {robot_name} state machine creating')
        # print(self.current_state.id)

    """" Entering state functions """
    def before_transition(self, event, state):
        self.last_state = self.current_state

    def on_enter_state(self, event, state):
        print(f"Entering '{state.id}' state from '{event}' event.")

    """" Entering state functions: END """

    """" Internal loop functions """

    def on_idle(self):
        pass
        # print('on_internal_idle')

    def on_waypoint_follower(self):
        print('on_waypoint_follower')

    """" Internal loop functions: END """

    """" Conditional functions """
    def no_obstacle_cond(self, event_data):
        print(event_data.transition)
        return event_data.transition.target == self.last_state

    def lost_line_cond(self):
        return not self.line_detected

    def found_line_cond(self):
        return self.line_detected

    def got_error(self):
        return self.err

    """" Conditional functions: END"""

    """" Validator functions"""

    def lost_line_validator(self):
        pass

    """" Validator functions: END"""


# In case of test this module
if __name__ == '__main__':

    robot_name = 'Vikings1'
    rsm = RobotStateTransition(robot_name=robot_name)

    graph = DotGraphMachine(RobotStateTransition)
    graph().write_png("test.png")

    rsm.turn_on()

    graph = DotGraphMachine(rsm)
    graph().write_png("test1.png")
