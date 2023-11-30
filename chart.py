import cdk8s
from config_map import create_config_map
from deployment import create_deployment
from service import create_service
class MyChart(cdk8s.Chart):
    def __init__(self, app: cdk8s.App, name: str):
        super().__init__(app, name)
        config_map = create_config_map(self)
        deployment = create_deployment(self, config_map)
        create_service(self, deployment)