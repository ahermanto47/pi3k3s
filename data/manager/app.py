import os
import random
import time
import paho.mqtt.client as mqtt
import docker

# Replace with your remote Swarm manager's details
remote_host = "10.0.0.200"
ssh_user = "admin"

# Create a client instance connecting via SSH
docker_client = docker.DockerClient(base_url=f"ssh://{ssh_user}@{remote_host}")


topic = os.environ.get("MQTT_TOPIC", "default/topic")

# Define the callback function for when a message is received
def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}")
    print(f"Message payload: {msg.payload.decode()}")
    # Process the received message here (one at a time)

    image_name = 'worker:0.1'  # Replace with your desired image

    service_name = f'my_swarm_job_{int(time.time() * 1000)}_{random.randint(0, 9999)}'
     
    # Create the service
    docker_client.services.create(
        image=image_name, 
        name=service_name,
        env=['DATA_DIR=/app/data/output/', f'TICKER={msg.payload.decode()}'],
        mounts=[docker.types.Mount(target='/app/data/output', source='/mnt/windows_share/output', type='bind')],
        # Set restart_policy to 'none' for one-shot tasks
        restart_policy=docker.types.RestartPolicy(condition='none'),
    )

    print(f"Service '{service_name}' created successfully!")

    # i = 2

    # while True:
    #     try:
    #         wait_time = 3 * 2 ** +i + random.randint(1, 10)
    #         print(f"Waiting for {wait_time} seconds before checking the service status...")
    #         time.sleep(wait_time)  # Wait before checking the service status
            
    #         service = docker_client.services.get(service_name)
            
    #         # Get all tasks for the service
    #         tasks = service.tasks()

    #         # Check the state of each task
    #         all_tasks_completed = True
    #         for task in tasks:
    #             task_id = task['ID']
    #             current_state = task['Status']['State']
    #             node = task['NodeID']
                
    #             print(f"Task ID: {task_id}, State: {current_state}, Node: {node}")

    #             if current_state != 'complete': # 1.8.5
    #                 all_tasks_completed = False
    #                 break # Exit loop if any task is not complete

    #         if all_tasks_completed:
    #             print(f"Service '{service_name}' has completed its execution (all tasks are 'complete').")
    #             # You might then choose to remove the service here
    #             service.remove()
    #             return False
    #         else:
    #             print(f"Service '{service_name}' is still executing or has failed tasks.")

    #     except docker.errors.NotFound:
    #         print(f"Service '{service_name}' not found.")
    #     except docker.errors.APIError as e:
    #         print(f"Error accessing service tasks for '{service_name}': {e}")


# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Set the on_message callback function
mqtt_client.on_message = on_message

# Connect to the MQTT broker
# Replace "broker_address" and "port" with your actual broker details
mqtt_client.connect("10.0.0.120", 1883, 60)

# Subscribe to the topic you want to receive messages from
# Replace "your/topic" with the actual topic
mqtt_client.subscribe(topic)

# Start the client loop to process incoming messages and callbacks
mqtt_client.loop_forever() # Use loop_forever() for a blocking loop
                      # or loop_start() for a non-blocking loop

# Disconnect from the broker (only reached if loop_forever() is exited)
mqtt_client.disconnect()
