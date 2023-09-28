"""

"""
from statemachine import State
from statemachine import StateMachine

from robot_model import RobotModel


class RobotStateTransition(StateMachine, RobotModel):
    # States
    start = State(initial=True)      # Turning on robot
    idle = State()                      # Robot on magnetic line, ready to receive command
    idle_lost = State()                 # Robot has lost magnetic line
    remote_control = State()                        # Remote control
    waypoint_follower = State()         # Executing mission by waypoints (mission pan unclear)
    approach_charger = State()          # Executing mission to drive close to charger
    at_charger = State()                # Robot is at front of charger, but it does not mean it is charging
    deapproach_charger = State()        # Executing mission to drove off from charger
    end = State(final=True)               # Shutting down robot
    error = State()                     # Error state - any error (BLDC lost, lidar lost, ...)

    """ Transitions """
    # Self transitions
    internal_start = start.to.itself(internal=True, on='on_idle')
    internal_idle = idle.to.itself(internal=True, on='on_idle')
    internal_idle_lost = idle_lost.to.itself(internal=True, on='on_idle')
    internal_remote_control = remote_control.to.itself(internal=True, on='on_idle')
    internal_waypoint_follower = waypoint_follower.to.itself(internal=True, on='on_idle')
    internal_approach_charger = approach_charger.to.itself(internal=True, on='on_idle')
    internal_at_charger = at_charger.to.itself(internal=True, on='on_idle')
    internal_deapproach_charger = deapproach_charger.to.itself(internal=True, on='on_idle')
    internal_error = error.to.itself(internal=True, on='on_idle')

    #st = start.to(start)

    # Manual transitions from specific states
    """ From START state """
    initialize = start.to(idle)
    got_error_at_start = start.to(error)
    got_end_at_start = start.to(end)

    """ From IDLE state """
    lost_line = idle.to(idle_lost)
    got_error_idle = idle.to(error)
    execute_waypoint_follower = idle.to(waypoint_follower)
    rc_idle = idle.to(remote_control)
    execute_approach_charger = idle.to(approach_charger)
    idle_to_at_charger = idle.to(at_charger)
    got_end_at_idle = idle.to(end)

    found_line = idle_lost.to(idle)
    got_error_idle_lost = idle_lost.to(error)
    rc_idle_lost = idle_lost.to(remote_control)
    got_end_at_idle_lost = idle_lost.to(end)

    got_error_remote_control = remote_control.to(error)
    to_idle_remote_control = remote_control.to(idle)
    got_end_at_remote_control = remote_control.to(end)

    finish_waypoint_follower = waypoint_follower.to(idle)
    got_error_waypoint_follower = waypoint_follower.to(error)
    got_end_at_waypoint_follower = waypoint_follower.to(end)

    finish_approach_charger = approach_charger.to(at_charger)
    cancel_approach_charger = approach_charger.to(idle)
    got_error_approach_charger = approach_charger.to(error)
    got_end_at_approach_charger = approach_charger.to(end)

    rc_at_charger = at_charger.to(remote_control)
    execute_deapproach_charger = at_charger.to(deapproach_charger)
    got_error_at_charger = at_charger.to(error)
    got_end_at_charger= at_charger.to(end)

    finish_deapproach_charger = deapproach_charger.to(idle)
    got_error_deapproach_charger = deapproach_charger.to(error)
    got_end_at_deapproach_charger = deapproach_charger.to(end)

    no_error = error.to(idle)
    rc_at_error = error.to(remote_control)
    got_end_at_error = error.to(end)

    # Manual transition to specific states
    to_idle = initialize | found_line | to_idle_remote_control | finish_waypoint_follower | \
                            cancel_approach_charger | finish_deapproach_charger | no_error
    to_idle_lost = lost_line
    to_remote_control = rc_idle | rc_idle_lost | rc_at_charger | rc_at_error
    to_waypoint_follower = execute_waypoint_follower
    to_approach_charger = execute_approach_charger
    to_at_charger = finish_approach_charger | idle_to_at_charger
    to_deapproach_charger = execute_deapproach_charger
    to_end = got_end_at_start | got_end_at_idle | got_end_at_idle_lost | got_end_at_remote_control | \
            got_end_at_waypoint_follower | got_end_at_approach_charger | got_end_at_charger | \
            got_end_at_deapproach_charger | got_end_at_error
    to_error = got_error_at_start | got_error_idle | got_error_idle_lost | got_error_remote_control | \
               got_error_waypoint_follower | got_error_approach_charger | got_error_at_charger | \
               got_error_deapproach_charger

    internal_cycle = internal_start | internal_idle | internal_idle_lost | internal_remote_control | \
                     internal_waypoint_follower | internal_approach_charger | internal_at_charger | \
                     internal_deapproach_charger | internal_error

    """ Transitions: END """

    def __init__(self, robot_name = 'robot_'):
        StateMachine.__init__(self)
        RobotModel.__init__(self, robot_name)

        print(f'Robot {robot_name} state machine creating')
        # print(self.current_state.id)

    """" Entering state functions """
    def on_enter_state(self, event, state):
        print(f"Entering '{state.id}' state from '{event}' event.")


    """" Entering state functions: END """

    """" Internal loop functions """
    def on_idle(self):
        pass
        #print('on_internal_idle')

    def on_waypoint_follower(self):
        print('on_waypoint_follower')

    """" Internal loop functions: END """

    """" Conditional functions """
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




