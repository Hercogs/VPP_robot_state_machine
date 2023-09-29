# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# https://stackoverflow.com/questions/474528/how-to-repeatedly-execute-a-function-every-x-seconds
# https://python-course.eu/applications-python/finite-state-machine.php
# https://github.com/fgmacedo/python-statemachine

# https://realpython.com/async-io-python/

from statemachine import State
from statemachine import StateMachine
from robot_state_machine import RobotStateTransition
from statemachine.contrib.diagram import DotGraphMachine


robot_name = 'Vikings1'
rsm = RobotStateTransition(robot_name=robot_name)

# Generate state machine graph
graph = DotGraphMachine(RobotStateTransition)
graph().write_png("initial_state_machine.png")

# Get all states
rsm_states = [state.value for state in rsm.states]

# Get all transitions
rsm_transitions_unfiltered = [[tr.event for tr in transitions_list.transitions] for transitions_list in rsm.states]
rsm_transitions = set()
for i in rsm_transitions_unfiltered:
    for j in i:
        rsm_transitions.add(j)


print(f'\nRobot has following states: {rsm_states}')
print(f'Robot has following transitions: {rsm_transitions}\n')
print(f'To switch between states, use command transitions.')

while True:
    transition_cmd = input(f'Enter transition (current state: {rsm.current_state.value}): ')

    if not transition_cmd:
        # If empty input, generate graph
        graph = DotGraphMachine(rsm)
        graph().write_png("current_state_machine.png")
    elif transition_cmd in rsm_transitions:
        try:
            rsm.send(transition_cmd)
        except Exception as ex:
            print(f'Error: {ex}')
    else:
        print('Invalid input, state transitions does not exist')
