import cdk8s_plus_26 as kplus # Import the cdk8s+ library which provides high-level constructs for Kubernetes
import cdk8s # Import the cdk8s library which is a framework to define Kubernetes YAML files using Python
import os  

app = cdk8s.App()  #Initialize a new cdk8s application
chart = cdk8s.Chart(app, "tech-test") # Create a new cdk8s chart within the application, acting like package of Kubernetes resources

site_contents_dict = {
    #Reads all the files within ./public and 
    #then add them to the site_contents_dict
    filename: open(os.path.join("./public", filename)).read() 
    for filename in os.listdir("./public")
}

#Create a Kubernetes ConfigMap in the chart, which stores configuration data that can be used by pods
config_map = kplus.ConfigMap(
    chart,
    "configmap",
    data=site_contents_dict, # The actual data of the ConfigMap, uses the dict from earlier.
    metadata=cdk8s.ApiObjectMetadata(name="tech-test-configmap"),
)

#Volume from config map so that data is available to the pods
volume = kplus.Volume.from_config_map(chart, "volume", config_map=config_map)

# Create a Kubernetes Deployment in the chart, which will ensure a specified number of replicas of a pod are running
deployment = kplus.Deployment(
    chart,
    "deployment",
    metadata=cdk8s.ApiObjectMetadata(
        name="tech-test-deployment",
    ),
    replicas=5 #Additional task have 5 replicas not default 2
)

liveness_probe = kplus.Probe.from_http_get(
    path="/",
    port=80,
    initial_delay_seconds=cdk8s.Duration.seconds(30),
    period_seconds=cdk8s.Duration.seconds(10),
    failure_threshold=3,  
)


# Add a container to the Deployment, specifying its properties
deployment.add_container(
    image="nginx:latest", #Docker image for container
    port=80, #Port container has exposed
    name="nginx",
    security_context=kplus.ContainerSecurityContextProps(
        ensure_non_root=False, read_only_root_filesystem=False #Security context for container had to set read_only to false to make it work
    ),
    volume_mounts=[
        kplus.VolumeMount(
            path="/usr/share/nginx/html", #Path where the volume is mounted in the container
            volume=volume,
        )
    ],
    liveness=liveness_probe
)

# Create a Kubernetes Service, which provides a stable endpoint for accessing the containers
service = kplus.Service(
    chart,
    "service",
    ports=[kplus.ServicePort(port=80, target_port=80)], #Port configuration for the service had to change this to access the site
    type=kplus.ServiceType.NODE_PORT,
    selector=deployment,
    metadata=cdk8s.ApiObjectMetadata(name="tech-test-service"),
)

# Entry point of the script, which generates the Kubernetes YAML files when the script is executed directly
if __name__ == "__main__":
    app.synth()
