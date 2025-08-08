from kubernetes import client
from kubernetes.client import Configuration, ApiClient
from kubernetes.client.rest import ApiException
import sys
import yaml

# === CONFIGURA QUI ===
API_SERVER = "https://192.168.3.17:6443"  # Modifica se diverso
NAMESPACE = "formazione-sou"
DEPLOYMENT_NAME = "formazione-sou-release-hello-node"
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVTelpPVnhweWFPOGljcTBBVXR3R1hsSl9pX1ZydUxFYnk3RnhlX1JsYXcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzU0MzIwNDg2LCJpYXQiOjE3NTQzMTY4ODYsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiMDZlYzA5MmMtMWU1ZS00ZTIxLTk4MmItN2IzMjFjOTkzYTJkIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJmb3JtYXppb25lLXNvdSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJyZWFkZXIiLCJ1aWQiOiJlZGExNTRlNi05MjJmLTQ2ZjQtODZlNS0zZDAwNjA1NGNmZmIifX0sIm5iZiI6MTc1NDMxNjg4Niwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmZvcm1hemlvbmUtc291OnJlYWRlciJ9.snUNbmko5mfgpwfZLnZngc2PuEY6y9WsN14hD4FQhE2D4Zcg3y0Ep_A9cAvDB2j9AETAuWjIJ7ew7KhT7IPZZxW9VtAarNLjqtVp2FoMvJwk1UJ_v-V2hhNT2UHyqrxwazTZLaAcWwDiYK1YHGvFF2qrt14vFRQg9JVsU-NqBl4I6N2pOuLuxIgPsMlZTINpsn_5M0gy_PUKgfD2oID3ykRI3KKz-oRiV9Ou8SWknn9ezURSjNt3l3VwfKtwzrhXWq-5O-Mzj6qODfhOL4SvLgFNGB8IsTqM7362YvVRkcEDJIPL_EWk6PuzSHB8Rs7WXsFHerqu9QZw8fXFd9fqqA"


def create_api_client(token, api_server):
    configuration = Configuration()
    configuration.host = api_server
    configuration.verify_ssl = False  # disattiva CA
    configuration.api_key = {"authorization": "Bearer " + token}
    return ApiClient(configuration)

def validate_container_obj(container):
    problems = []

    if not container.readiness_probe:
        problems.append("Missing readinessProbe")
    if not container.liveness_probe:
        problems.append("Missing livenessProbe")
    if not container.resources:
        problems.append("Missing resources block")
    else:
        if not container.resources.limits:
            problems.append("Missing resource limits")
        if not container.resources.requests:
            problems.append("Missing resource requests")
    return problems

def main():
    api_client = create_api_client(TOKEN, API_SERVER)
    apps_v1 = client.AppsV1Api(api_client)

    try:
        deployment = apps_v1.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)

        # Stampo il deployment in YAML
        deployment_dict = deployment.to_dict()
        print("--- Deployment YAML ---")
        print(yaml.dump(deployment_dict, sort_keys=False))

        # Validazione attributi richiesti per ogni container
        containers = deployment.spec.template.spec.containers
        for container in containers:
            issues = validate_container_obj(container)
            if issues:
                print(f"\n❌ Errori nel container '{container.name}':")
                for issue in issues:
                    print(f" - {issue}")
                sys.exit(1)

        print("\n✅ Tutti gli attributi richiesti sono presenti.")

    except ApiException as e:
        print(f"Errore API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

