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



# Run a transition
robot_name = 'Vikings1'
rsm = RobotStateTransition(robot_name=robot_name)

graph = DotGraphMachine(RobotStateTransition)
dot = graph()
graph().write_png("a.png")




# rsm_states = [state.value for state in rsm.states]

# # print(rsm.states[0])
# #
# print(f'\nRobot has following states: {rsm_states}')
# print(f'To switch between states, use command "state_name". For example, '
#       'to switch to idle, enter "idle". To switch to current state, enter nothing')
# print(f'Current state: {rsm.current_state.value}')

# while True:
#     next_state = input(f'Enter next state (current: {rsm.current_state.value}): ')

#     if not next_state:
#         rsm.internal_cycle()
#     elif next_state in rsm_states:
#         try:
#             rsm.send('to_' + next_state)
#         except Exception as ex:
#             print(f'Error: {ex}')
#     else:
#         print('Invalid input, state does not exist')
