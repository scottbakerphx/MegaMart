import requests

GRAFANA_URL = "http://localhost:3000"
PROMETHEUS_PORT = 9092  # Update this to your local Prometheus port (e.g., 9092)
AUTH = ("admin", "admin")
HEADERS = {"Content-Type": "application/json"}


def setup_prometheus_datasource():
    print("1. Creating Local Prometheus Datasource...")
    prom_url = f"http://localhost:{PROMETHEUS_PORT}"

    payload = {
        "name": "Prometheus",
        "type": "prometheus",
        "url": prom_url,
        "access": "proxy",
        "isDefault": True,
    }
    res = requests.post(
        f"{GRAFANA_URL}/api/datasources",
        auth=AUTH,
        json=payload,
        headers=HEADERS
    )
    if res.status_code in (200, 409):
        print(f"   Local Prometheus Datasource configured at {prom_url}")
    else:
        print(f"   Failed to add datasource: {res.status_code} - {res.text}")


def setup_drift_dashboard():
    print("2. Creating MegaMart ML Operations Dashboard...")
    payload = {
        "dashboard": {
            "id": None,
            "title": "MegaMart ML Operations",
            "tags": ["mlops", "drift"],
            "timezone": "browser",
            "panels": [
                {
                    "id": 1,
                    "title": "Feature Drift (PSI)",
                    "type": "timeseries",
                    "datasource": "Prometheus",
                    "targets": [
                        {
                            "expr": "max by (feature) (megamart_feature_psi)",
                            "legendFormat": "{{feature}}",
                            "refId": "A",
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "custom": {
                                "drawStyle": "line",
                                "lineInterpolation": "smooth",
                            },
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 0.1},
                                    {"color": "red", "value": 0.2},
                                ],
                            },
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                }
            ],
            "schemaVersion": 36,
            "version": 0,
        },
        "overwrite": True,
    }
    res = requests.post(
        f"{GRAFANA_URL}/api/dashboards/db",
        auth=AUTH,
        json=payload,
        headers=HEADERS
    )
    if res.status_code == 200:
        print("   Dashboard 'MegaMart ML Operations' created successfully!")
    else:
        print(f"   Failed to create dashboard: {res.status_code} - {res.text}")


def main():
    setup_prometheus_datasource()
    setup_drift_dashboard()


if __name__ == "__main__":
    main()