# This is a sample Python script.
import json

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# https://stackoverflow.com/questions/474528/how-to-repeatedly-execute-a-function-every-x-seconds
# https://python-course.eu/applications-python/finite-state-machine.php
# https://github.com/fgmacedo/python-statemachine

# https://realpython.com/async-io-python/


from robot_state_machine import RobotStateTransition
from statemachine.contrib.diagram import DotGraphMachine

import paho.mqtt.client as mqtt

IP = '85.254.224.137'
PORT = 8883


class RobotMqttCommunication:
    def __init__(self, ip: str, port: int):

        # Create mqtt client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(ip, port)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.subscribe()

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def subscribe(self):
        print('Subscribe to topics')

    def publish_msg(self, topic, payload=None, qos=0, retain=False):
        print(f'Publish msg: {payload}, on topic: {topic}')
        status = self.mqtt_client.publish(topic, payload, qos, retain)
        if status.rc == mqtt.MQTT_ERR_SUCCESS:
            print('mqtt.MQTT_ERR_SUCCESS')
        else:
            print(f'status.rc not OK: {status.rc}')
        if status.is_published():
            print('MSG published')


client = RobotMqttCommunication(IP, PORT)

# Loop MQTT client in separate thread
client.mqtt_client.loop_start()

# Create robot state machine
robot_name = 'Vikings1'
rsm = RobotStateTransition(robot_name=robot_name)

# Generate state machine graph
graph = DotGraphMachine(RobotStateTransition)
graph().write_png("images/initial_state_machine.png")

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
print(f'To switch between states, use command transitions.' \
      'Enter nothing, to generate state machine graph in present time')

while True:
    transition_cmd = input(f'Enter transition (current state: {rsm.current_state.value}): ')

    if not transition_cmd:
        # If empty input, generate graph
        graph = DotGraphMachine(rsm)
        graph().write_png("images/current_state_machine.png")
    elif transition_cmd in rsm_transitions:
        try:
            rsm.send(transition_cmd)
        except Exception as ex:
            print(f'Error: {ex}')
    else:
        print('Invalid input, state transitions does not exist')

    # Publish MQTT 'ping' message
    msg = {'sender': robot_name,
           'location': {'name': rsm.current_state.id}}
    msg_json = json.dumps(msg)
    print(msg_json)
    client.publish_msg(topic='ping', payload=msg_json)
