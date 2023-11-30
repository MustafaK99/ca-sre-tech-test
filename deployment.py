import cdk8s_plus_26 as kplus
import cdk8s
def create_deployment(chart: cdk8s.Chart, config_map: kplus.ConfigMap) -> kplus.Deployment:
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

    #Additional task 3
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
    return deployment