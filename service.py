import cdk8s_plus_26 as kplus
import cdk8s
def create_service(chart: cdk8s.Chart, deployment: kplus.Deployment) -> kplus.Service:
    service = kplus.Service(
        chart,
        "service",
        ports=[kplus.ServicePort(port=80, target_port=80)], #Port configuration for the service had to change this to access the site
        type=kplus.ServiceType.NODE_PORT,
        selector=deployment,
        metadata=cdk8s.ApiObjectMetadata(name="tech-test-service"),
    )
    return service