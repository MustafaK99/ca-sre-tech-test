import cdk8s
from chart import MyChart
app = cdk8s.App()
MyChart(app, "tech-test")
if __name__ == "__main__":
    app.synth()