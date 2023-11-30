import cdk8s_plus_26 as kplus
import cdk8s
import os
def create_config_map(chart: cdk8s.Chart) -> kplus.ConfigMap:
    site_contents_dict = {
        filename: open(os.path.join("./public", filename)).read()
        for filename in os.listdir("./public")
    }
    config_map = kplus.ConfigMap(
        chart,
        "configmap",
        data=site_contents_dict,
        metadata=cdk8s.ApiObjectMetadata(name="tech-test-configmap"),
    )
    return config_map