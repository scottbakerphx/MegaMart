import requests

GRAFANA_URL = "http://localhost:3000"
AUTH = ("admin", "admin")
HEADERS = {"Content-Type": "application/json"}


def get_prometheus_ds_uid():
    """Fetch active Prometheus datasource UID from Grafana."""
    res = requests.get(f"{GRAFANA_URL}/api/datasources", auth=AUTH)
    if res.status_code == 200:
        for ds in res.json():
            if ds.get("type") == "prometheus":
                return ds.get("uid")
    raise RuntimeError("No active Prometheus datasource found in Grafana!")


def ensure_folder():
    """Create or verify the MLOps folder."""
    folder_payload = {"uid": "mlops_folder", "title": "MLOps"}
    requests.post(
        f"{GRAFANA_URL}/api/folders",
        auth=AUTH,
        json=folder_payload,
        headers=HEADERS,
    )


def create_alert_rule(ds_uid):
    """Provision Unified Alert Rule for PSI > 0.2."""
    payload = {
        "title": "MegaMart Feature Drift Alert",
        "ruleGroup": "drift_monitoring",
        "folderUID": "mlops_folder",
        "condition": "C",
        "noDataState": "OK",
        "execErrState": "Alerting",
        "for": "0s",
        "data": [
            {
                "refId": "A",
                "queryType": "",
                "relativeTimeRange": {"from": 600, "to": 0},
                "datasourceUid": ds_uid,
                "model": {
                    "editorMode": "code",
                    "expr": "max by (feature) (megamart_feature_psi)",
                    "instant": True,
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "A",
                },
            },
            {
                "refId": "B",
                "datasourceUid": "-100",
                "model": {
                    "datasource": {"type": "__expr__", "uid": "-100"},
                    "expression": "A",
                    "reducer": "max",
                    "type": "reduce",
                    "refId": "B",
                },
            },
            {
                "refId": "C",
                "datasourceUid": "-100",
                "model": {
                    "datasource": {"type": "__expr__", "uid": "-100"},
                    "expression": "B",
                    "type": "threshold",
                    "conditions": [
                        {
                            "evaluator": {"params": [0.2], "type": "gt"}
                        }
                    ],
                    "refId": "C",
                },
            },
        ],
        "annotations": {
            "summary": "Significant feature drift detected (PSI > 0.2)",
            "description": "Data drift exceeds safety limit (0.2). Triggering model re-validation.",
        },
        "labels": {"severity": "critical", "team": "mlops"},
    }

    res = requests.post(
        f"{GRAFANA_URL}/api/v1/provisioning/alert-rules",
        auth=AUTH,
        json=payload,
        headers=HEADERS,
    )

    if res.status_code in (200, 201):
        print("[✔] Alert Rule provisioned successfully!")
    else:
        print(f"[✘] Alert provision failed ({res.status_code}): {res.text}")


def main():
    try:
        ds_uid = get_prometheus_ds_uid()
        ensure_folder()
        create_alert_rule(ds_uid)
    except Exception as e:
        print(f"[✘] Error: {e}")


if __name__ == "__main__":
    main()