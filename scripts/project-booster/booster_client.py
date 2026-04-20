"""Project Booster API client.

Thin wrapper around the Project Booster REST API (v2.15).
Handles authentication, pagination, retry on rate-limit, and error handling.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from .config import BoosterConfig


class BoosterAPIError(Exception):
    """Raised when the API returns a non-2xx status."""

    def __init__(self, status_code: int, body: dict | str):
        self.status_code = status_code
        self.body = body
        if isinstance(body, dict):
            msg = body.get("message", str(body))
        else:
            msg = str(body)
        super().__init__(f"HTTP {status_code}: {msg}")


class UntrustedCertificateError(BoosterAPIError):
    """Raised when the API returns 502 with untrustedCertificate flag."""

    def __init__(self, body: dict | str):
        super().__init__(502, body)


class BoosterClient:
    """Client for the Project Booster backend API."""

    MAX_RETRIES = 3
    RETRY_BACKOFF = 2  # seconds base for exponential backoff

    def __init__(self, config: BoosterConfig):
        self._config = config
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {config.token}",
                "Accept": "application/json",
            }
        )
        self._session.verify = config.ssl_verify

    @property
    def api_url(self) -> str:
        return self._config.api_url

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self.api_url}{path}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json_body: Any = None,
        retries: int | None = None,
    ) -> requests.Response:
        max_retries = retries if retries is not None else self.MAX_RETRIES
        attempt = 0
        while True:
            resp = self._session.request(
                method, self._url(path), params=params, json=json_body
            )
            # Rate-limit handling (429)
            if resp.status_code == 429 and attempt < max_retries:
                retry_after = int(
                    resp.headers.get("Retry-After", self.RETRY_BACKOFF * (2 ** attempt))
                )
                time.sleep(retry_after)
                attempt += 1
                continue

            if resp.status_code >= 400:
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text
                # Detect untrusted certificate error (502 + flag)
                if (
                    resp.status_code == 502
                    and isinstance(body, dict)
                    and body.get("untrustedCertificate")
                ):
                    raise UntrustedCertificateError(body)
                raise BoosterAPIError(resp.status_code, body)
            return resp

    def _get(self, path: str, **params: Any) -> Any:
        resp = self._request("GET", path, params=params or None)
        if resp.status_code == 204:
            return None
        return resp.json()

    def _post(self, path: str, body: Any = None, **params: Any) -> Any:
        resp = self._request("POST", path, params=params or None, json_body=body)
        if resp.status_code in (201, 202):
            try:
                return resp.json()
            except Exception:
                return {"location": resp.headers.get("Location")}
        if resp.status_code == 204:
            return None
        return resp.json()

    def _put(self, path: str, body: Any = None, **params: Any) -> Any:
        resp = self._request("PUT", path, params=params or None, json_body=body)
        if resp.status_code == 204:
            return None
        return resp.json()

    def _patch(self, path: str, body: Any = None) -> Any:
        resp = self._request("PATCH", path, json_body=body)
        if resp.status_code == 204:
            return None
        return resp.json()

    def _delete(self, path: str, **params: Any) -> Any:
        resp = self._request("DELETE", path, params=params or None)
        if resp.status_code in (200, 202, 204):
            if resp.status_code == 204 or not resp.text.strip():
                return None
            try:
                return resp.json()
            except Exception:
                return None
        return resp.json()

    # ------------------------------------------------------------------
    # Index
    # ------------------------------------------------------------------

    def index(self) -> dict:
        """GET /api — returns API index with links."""
        return self._get("")

    # ------------------------------------------------------------------
    # Current user
    # ------------------------------------------------------------------

    def get_current_user(self) -> dict:
        """GET /api/users/current"""
        return self._get("/users/current")

    def logout(self) -> None:
        """DELETE /api/users/current — logout / clear cached user data."""
        self._delete("/users/current")

    # ------------------------------------------------------------------
    # User profile
    # ------------------------------------------------------------------

    def get_profile(self) -> dict:
        """GET /api/users/current/profile"""
        return self._get("/users/current/profile")

    def update_profile(self, profile: dict) -> dict:
        """PUT /api/users/current/profile"""
        return self._put("/users/current/profile", profile)

    # ------------------------------------------------------------------
    # Trusted certificates
    # ------------------------------------------------------------------

    def list_trusted_certificates(self, page: int = 0, size: int = 20) -> dict:
        """GET /api/users/current/trusted-certificates (paginated)."""
        return self._get("/users/current/trusted-certificates", page=page, size=size)

    def add_trusted_certificate(self, pem: str) -> dict:
        """POST /api/users/current/trusted-certificates"""
        return self._post("/users/current/trusted-certificates", {"pem": pem})

    def delete_trusted_certificate(self, cert_id: int) -> None:
        """DELETE /api/users/current/trusted-certificates/{id}"""
        self._delete(f"/users/current/trusted-certificates/{cert_id}")

    # ------------------------------------------------------------------
    # Secrets
    # ------------------------------------------------------------------

    def create_secret(self, key: str, value: str, secret_type: str, label: str) -> dict:
        """POST /api/users/current/secrets"""
        return self._post(
            "/users/current/secrets",
            {"key": key, "value": value, "type": secret_type, "label": label},
        )

    def list_secrets(self) -> list[dict]:
        """GET /api/users/current/secrets"""
        return self._get("/users/current/secrets")

    def get_secret(self, secret_id: int) -> dict:
        """GET /api/users/current/secrets/{id}"""
        return self._get(f"/users/current/secrets/{secret_id}")

    def delete_secret(self, secret_id: int) -> None:
        """DELETE /api/users/current/secrets/{id}"""
        self._delete(f"/users/current/secrets/{secret_id}")

    # ------------------------------------------------------------------
    # Ratings
    # ------------------------------------------------------------------

    def get_rating(self) -> dict:
        """GET /api/users/current/rating"""
        return self._get("/users/current/rating")

    def save_rating(self, rating: dict) -> dict:
        """POST /api/users/current/rating"""
        return self._post("/users/current/rating", rating)

    # ------------------------------------------------------------------
    # Scenarios
    # ------------------------------------------------------------------

    def create_scenario(
        self,
        scenario_type: str,
        version: str | None = None,
        inputs: dict | None = None,
    ) -> dict:
        """POST /api/scenarios — create a new scenario."""
        body: dict[str, Any] = {"scenarioType": scenario_type}
        if version:
            body["version"] = version
        if inputs:
            body["inputs"] = inputs
        return self._post("/scenarios", body)

    def duplicate_scenario(self, scenario_id: int) -> dict:
        """POST /api/scenarios/{id} — duplicate an existing scenario."""
        return self._post(f"/scenarios/{scenario_id}")

    def list_scenarios(
        self,
        page: int = 0,
        size: int = 20,
        sort: str = "lastModifiedAt,desc",
        archived: bool | None = None,
    ) -> dict:
        """GET /api/scenarios — paginated list of user's scenarios."""
        params: dict[str, Any] = {"page": page, "size": size, "sort": sort}
        if archived is not None:
            params["archived"] = str(archived).lower()
        return self._get("/scenarios", **params)

    def list_all_scenarios(
        self,
        page: int = 0,
        size: int = 20,
        sort: str = "lastModifiedAt,desc",
        pipeline_status: str | None = None,
    ) -> dict:
        """GET /api/scenarios/all — admin: list all scenarios."""
        params: dict[str, Any] = {"page": page, "size": size, "sort": sort}
        if pipeline_status:
            params["pipelineStatus"] = pipeline_status
        return self._get("/scenarios/all", **params)

    def get_scenario(self, scenario_id: int) -> dict:
        """GET /api/scenarios/{id} — scenario details."""
        return self._get(f"/scenarios/{scenario_id}")

    def update_scenario(
        self,
        scenario_id: int,
        scenario_type: str,
        version: str | None = None,
        inputs: dict | None = None,
    ) -> dict:
        """PUT /api/scenarios/{id} — full update."""
        body: dict[str, Any] = {"scenarioType": scenario_type}
        if version:
            body["version"] = version
        if inputs:
            body["inputs"] = inputs
        return self._put(f"/scenarios/{scenario_id}", body)

    def patch_scenario(self, scenario_id: int, archived: bool) -> dict:
        """PATCH /api/scenarios/{id} — archive/unarchive."""
        return self._patch(f"/scenarios/{scenario_id}", {"archived": archived})

    def delete_scenario(self, scenario_id: int) -> None:
        """DELETE /api/scenarios/{id}"""
        self._delete(f"/scenarios/{scenario_id}")

    def get_scenario_scopes(self, scenario_id: int) -> dict:
        """GET /api/scenarios/{id}/scopes — admin: get scenario scopes."""
        return self._get(f"/scenarios/{scenario_id}/scopes")

    def get_scenario_children(self, scenario_id: int) -> list[dict]:
        """GET /api/scenarios/{id}/children — child scenarios."""
        return self._get(f"/scenarios/{scenario_id}/children")

    # ------------------------------------------------------------------
    # Pipelines
    # ------------------------------------------------------------------

    def create_pipeline(
        self, scenario_id: int, skip_previously_failed: bool = False
    ) -> dict:
        """POST /api/scenarios/{id}/pipeline — trigger a pipeline execution."""
        return self._post(
            f"/scenarios/{scenario_id}/pipeline",
            skipPreviouslyFailedActions=str(skip_previously_failed).lower(),
        )

    def get_pipeline(self, scenario_id: int) -> dict:
        """GET /api/scenarios/{id}/pipeline — pipeline status & actions."""
        return self._get(f"/scenarios/{scenario_id}/pipeline")

    def cancel_pipeline(self, scenario_id: int) -> None:
        """DELETE /api/scenarios/{id}/pipeline — cancel a running pipeline."""
        self._delete(f"/scenarios/{scenario_id}/pipeline")

    def get_pipeline_credentials(self, scenario_id: int) -> list[dict]:
        """GET /api/scenarios/{id}/pipeline/credentials"""
        return self._get(f"/scenarios/{scenario_id}/pipeline/credentials")

    def wait_for_pipeline(
        self, scenario_id: int, poll_interval: int = 10, timeout: int = 600
    ) -> dict:
        """Poll pipeline status until completion or timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            pipeline = self.get_pipeline(scenario_id)
            status = pipeline.get("status", "").upper()
            if status in ("COMPLETED", "FAILED", "CANCELLED"):
                return pipeline
            time.sleep(poll_interval)
        raise TimeoutError(
            f"Pipeline for scenario {scenario_id} did not finish within {timeout}s"
        )

    # ------------------------------------------------------------------
    # Orchestrators — namespaces & environments
    # ------------------------------------------------------------------

    def check_orchestrator(
        self, orch_type: str, url: str | None = None, ssl_no_verify: bool = False
    ) -> dict:
        """GET /api/orchestrators/{type} — check connection to orchestrator."""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._get(f"/orchestrators/{orch_type}", **params)

    def list_namespaces(
        self,
        orch_type: str,
        url: str | None = None,
        page: int = 0,
        size: int = 20,
        ssl_no_verify: bool = False,
        full_description: bool = True,
        role_bindings: bool = False,
    ) -> dict:
        """GET /api/orchestrators/{type}/namespaces"""
        params: dict[str, Any] = {
            "page": page,
            "size": size,
            "sslNoVerify": str(ssl_no_verify).lower(),
            "fullDescription": str(full_description).lower(),
            "roleBindings": str(role_bindings).lower(),
        }
        if url:
            params["url"] = url
        return self._get(f"/orchestrators/{orch_type}/namespaces", **params)

    def test_namespace_creation(
        self,
        orch_type: str,
        name: str,
        url: str | None = None,
        ssl_no_verify: bool = False,
    ) -> dict:
        """POST /api/orchestrators/{type}/namespaces — test if namespace can be created."""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._post(
            f"/orchestrators/{orch_type}/namespaces", {"name": name}, **params
        )

    def test_namespace_writable(
        self,
        orch_type: str,
        name: str,
        url: str | None = None,
        ssl_no_verify: bool = False,
    ) -> dict:
        """PUT /api/orchestrators/{type}/namespaces — test if namespace is writable."""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._put(
            f"/orchestrators/{orch_type}/namespaces", {"name": name}, **params
        )

    def list_namespaces_resources(
        self,
        orch_type: str,
        url: str | None = None,
        page: int = 0,
        size: int = 20,
        ssl_no_verify: bool = False,
        role_bindings: bool = False,
    ) -> dict:
        """GET /api/orchestrators/{type}/namespaces-resources"""
        params: dict[str, Any] = {
            "page": page,
            "size": size,
            "sslNoVerify": str(ssl_no_verify).lower(),
            "roleBindings": str(role_bindings).lower(),
        }
        if url:
            params["url"] = url
        return self._get(
            f"/orchestrators/{orch_type}/namespaces-resources", **params
        )

    def create_role_binding(
        self,
        orch_type: str,
        namespace: str,
        body: dict,
        url: str | None = None,
        ssl_no_verify: bool = False,
    ) -> dict:
        """POST /api/orchestrators/{type}/namespaces/{namespace}/role-binding"""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._post(
            f"/orchestrators/{orch_type}/namespaces/{namespace}/role-binding",
            body,
            **params,
        )

    def create_quotas(
        self,
        orch_type: str,
        namespace: str,
        body: dict,
        url: str | None = None,
        ssl_no_verify: bool = False,
    ) -> dict:
        """POST /api/orchestrators/{type}/namespaces/{namespace}/quotas"""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._post(
            f"/orchestrators/{orch_type}/namespaces/{namespace}/quotas",
            body,
            **params,
        )

    def list_namespace_services(
        self,
        orch_type: str,
        namespace: str,
        url: str | None = None,
        page: int = 0,
        size: int = 20,
        ssl_no_verify: bool = False,
    ) -> dict:
        """GET /api/orchestrators/{type}/namespaces/{namespace}/services"""
        params: dict[str, Any] = {
            "page": page,
            "size": size,
            "sslNoVerify": str(ssl_no_verify).lower(),
        }
        if url:
            params["url"] = url
        return self._get(
            f"/orchestrators/{orch_type}/namespaces/{namespace}/services", **params
        )

    def get_service(
        self,
        orch_type: str,
        namespace: str,
        release_name: str,
        url: str | None = None,
        ssl_no_verify: bool = False,
    ) -> dict:
        """GET /api/orchestrators/{type}/namespaces/{ns}/services/{releaseName}"""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._get(
            f"/orchestrators/{orch_type}/namespaces/{namespace}/services/{release_name}",
            **params,
        )

    def get_namespace_details(
        self,
        orch_type: str,
        namespace: str,
        url: str | None = None,
        ssl_no_verify: bool = False,
    ) -> dict:
        """GET /api/orchestrators/{type}/namespaces/{namespace}"""
        params: dict[str, Any] = {"sslNoVerify": str(ssl_no_verify).lower()}
        if url:
            params["url"] = url
        return self._get(
            f"/orchestrators/{orch_type}/namespaces/{namespace}", **params
        )

    def list_all_services(
        self,
        orch_type: str,
        url: str | None = None,
        page: int = 0,
        size: int = 20,
        ssl_no_verify: bool = False,
    ) -> dict:
        """GET /api/orchestrators/{type}/services"""
        params: dict[str, Any] = {
            "page": page,
            "size": size,
            "sslNoVerify": str(ssl_no_verify).lower(),
        }
        if url:
            params["url"] = url
        return self._get(f"/orchestrators/{orch_type}/services", **params)

    # ------------------------------------------------------------------
    # Artifactory
    # ------------------------------------------------------------------

    def list_artifactory_repos(
        self,
        url: str | None = None,
        repo_type: str | None = None,
        package_type: str | None = None,
        page: int = 0,
        size: int = 20,
    ) -> dict:
        """GET /api/artifactory/repositories"""
        params: dict[str, Any] = {"page": page, "size": size}
        if url:
            params["url"] = url
        if repo_type:
            params["type"] = repo_type
        if package_type:
            params["packageType"] = package_type
        return self._get("/artifactory/repositories", **params)

    def create_artifactory_repos(
        self,
        body: dict,
        url: str | None = None,
        package_type: str | None = None,
    ) -> dict:
        """POST /api/artifactory/repositories"""
        params: dict[str, Any] = {}
        if url:
            params["url"] = url
        if package_type:
            params["packageType"] = package_type
        return self._post("/artifactory/repositories", body, **params)

    # ------------------------------------------------------------------
    # Certificates
    # ------------------------------------------------------------------

    def list_certificates(self, url: str) -> dict:
        """GET /api/certificates?url=..."""
        return self._get("/certificates", url=url)

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------

    def get_config(self) -> dict:
        """GET /api/config"""
        return self._get("/config")

    def reload_config(self, branch: str | None = None) -> dict:
        """PUT /api/config — admin: reload configuration."""
        params: dict[str, Any] = {}
        if branch:
            params["branch"] = branch
        return self._put("/config", **params)

    def reset_config(self) -> None:
        """DELETE /api/config — admin: reset & reload configuration."""
        self._delete("/config")

    def get_auth_config(self) -> dict:
        """GET /api/config/authentication — public OAuth2 auth config."""
        return self._get("/config/authentication")

    def list_banners(self) -> dict:
        """GET /api/config/banners"""
        return self._get("/config/banners")

    def create_banner(self, body: dict) -> dict:
        """POST /api/config/banners — admin: create a banner."""
        return self._post("/config/banners", body)

    # ------------------------------------------------------------------
    # Metrics (admin)
    # ------------------------------------------------------------------

    def get_connection_metrics(self, page: int = 0, size: int = 20) -> dict:
        """GET /api/metrics/connections — admin: connection metrics."""
        return self._get("/metrics/connections", page=page, size=size)

    def get_usage_metrics(self) -> dict:
        """GET /api/metrics/usage — admin: usage metrics."""
        return self._get("/metrics/usage")

    def get_rating_metrics(self, page: int = 0, size: int = 20) -> dict:
        """GET /api/metrics/ratings — admin: all user ratings."""
        return self._get("/metrics/ratings", page=page, size=size)

    # ------------------------------------------------------------------
    # High-level helpers — scenario types discovery
    # ------------------------------------------------------------------

    SCENARIO_TYPES = {
        "new_web_app": "Create a new web application (mono or multi-component)",
        "new_web_doc": "Create a new static documentation site (GitLab Pages)",
        "new_tool": "Deploy a tool/service (Nexus, Vault, SonarQube, …)",
        "update_service": "Update an existing deployed service",
        "new_database": "Deploy a standalone database",
        "update_database": "Update an existing database",
        "new_launchpad": "Deploy infrastructure on cloud (Azure, AWS, AzureStack)",
        "new_repository": "Create a new Artifactory repository",
        "configure_kube_green_for_service": "Configure Kube-Green on Arcus",
        "configure_kube_green_for_app": "Configure Kube-Green on InnerShift",
        "configure_kasten_for_service": "Configure Kasten backup on Arcus",
        "configure_kasten_for_app": "Configure Kasten backup on InnerShift",
        "remove_resources_for_service": "Remove resources from Innersource + Arcus",
        "remove_resources_for_application": "Remove resources from Innersource + InnerShift",
    }

    def get_scenario_types(self) -> dict:
        """Fetch available scenario types from the platform config.

        Calls GET /api/config and extracts scenarioDefinitionGroups.
        Falls back to the built-in SCENARIO_TYPES catalog.
        """
        config = self.get_config()
        groups = config.get("scenarioDefinitionGroups")
        if groups:
            return groups
        return self.SCENARIO_TYPES

    # ------------------------------------------------------------------
    # High-level helpers — convenience scenario builders
    # ------------------------------------------------------------------

    def create_database(
        self,
        db_type: str,
        namespace: str,
        *,
        orch_type: str = "innershift",
        extra_inputs: dict | None = None,
    ) -> dict:
        """Create a database scenario with pre-filled inputs.

        Args:
            db_type: One of postgresql, mysql, mongodb, elasticsearch.
            namespace: Target namespace on the orchestrator.
            orch_type: Orchestrator type (innershift, arcus).
            extra_inputs: Additional input fields to merge.

        Returns:
            The created scenario dict.
        """
        inputs: dict[str, Any] = {
            "databaseType": db_type,
            "namespace": namespace,
            "orchestratorType": orch_type,
        }
        if extra_inputs:
            inputs.update(extra_inputs)
        return self.create_scenario("new_database", inputs=inputs)

    def create_app(
        self,
        app_name: str,
        namespace: str,
        *,
        orch_type: str = "innershift",
        components: list[dict] | None = None,
        extra_inputs: dict | None = None,
    ) -> dict:
        """Create a web application scenario with pre-filled inputs.

        Args:
            app_name: Application name.
            namespace: Target namespace.
            orch_type: Orchestrator type.
            components: List of component dicts (backend/frontend definitions).
            extra_inputs: Additional input fields to merge.

        Returns:
            The created scenario dict.
        """
        inputs: dict[str, Any] = {
            "applicationName": app_name,
            "namespace": namespace,
            "orchestratorType": orch_type,
        }
        if components:
            inputs["components"] = components
        if extra_inputs:
            inputs.update(extra_inputs)
        return self.create_scenario("new_web_app", inputs=inputs)

    def create_tool(
        self,
        tool_type: str,
        namespace: str,
        *,
        orch_type: str = "arcus",
        extra_inputs: dict | None = None,
    ) -> dict:
        """Create a tool/service scenario.

        Args:
            tool_type: Tool to deploy (nexus, vault, sonarqube, …).
            namespace: Target namespace.
            orch_type: Orchestrator type.
            extra_inputs: Additional input fields to merge.

        Returns:
            The created scenario dict.
        """
        inputs: dict[str, Any] = {
            "toolType": tool_type,
            "namespace": namespace,
            "orchestratorType": orch_type,
        }
        if extra_inputs:
            inputs.update(extra_inputs)
        return self.create_scenario("new_tool", inputs=inputs)

    # ------------------------------------------------------------------
    # High-level helpers — full deployment flow
    # ------------------------------------------------------------------

    def deploy(
        self,
        scenario_type: str,
        inputs: dict,
        *,
        version: str | None = None,
        skip_previously_failed: bool = False,
        poll_interval: int = 10,
        timeout: int = 600,
        on_status: Any = None,
    ) -> dict:
        """End-to-end: create scenario → trigger pipeline → wait → return result.

        Args:
            scenario_type: One of the SCENARIO_TYPES keys.
            inputs: Scenario input dict.
            version: Optional scenario version.
            skip_previously_failed: Skip actions that failed in a previous run.
            poll_interval: Seconds between status polls.
            timeout: Max seconds to wait for pipeline completion.
            on_status: Optional callback(pipeline_dict) called on each poll.

        Returns:
            Dict with keys: scenario, pipeline, credentials.

        Raises:
            TimeoutError: If pipeline doesn't complete within timeout.
            BoosterAPIError: On API errors.
        """
        # 1. Create scenario
        scenario = self.create_scenario(scenario_type, version=version, inputs=inputs)
        scenario_id = scenario["id"]

        # 2. Trigger pipeline
        self.create_pipeline(scenario_id, skip_previously_failed=skip_previously_failed)

        # 3. Wait for completion
        deadline = time.time() + timeout
        pipeline = {}
        while time.time() < deadline:
            pipeline = self.get_pipeline(scenario_id)
            status = pipeline.get("status", "").upper()
            if on_status:
                on_status(pipeline)
            if status in ("COMPLETED", "FAILED", "CANCELLED"):
                break
            time.sleep(poll_interval)
        else:
            raise TimeoutError(
                f"Pipeline for scenario {scenario_id} did not finish within {timeout}s"
            )

        # 4. Fetch credentials if completed
        credentials = []
        if pipeline.get("status", "").upper() == "COMPLETED":
            try:
                credentials = self.get_pipeline_credentials(scenario_id)
            except BoosterAPIError:
                pass  # Some scenarios don't produce credentials

        return {
            "scenario": scenario,
            "pipeline": pipeline,
            "credentials": credentials,
        }

    def deploy_database(
        self,
        db_type: str,
        namespace: str,
        *,
        orch_type: str = "innershift",
        extra_inputs: dict | None = None,
        poll_interval: int = 10,
        timeout: int = 600,
        on_status: Any = None,
    ) -> dict:
        """Deploy a database end-to-end: create → pipeline → wait → credentials.

        Args:
            db_type: postgresql, mysql, mongodb, or elasticsearch.
            namespace: Target namespace.
            orch_type: Orchestrator type (innershift, arcus).
            extra_inputs: Additional input fields.
            poll_interval: Seconds between polls.
            timeout: Max wait seconds.
            on_status: Optional callback(pipeline_dict).

        Returns:
            Dict with scenario, pipeline, and credentials.
        """
        inputs: dict[str, Any] = {
            "databaseType": db_type,
            "namespace": namespace,
            "orchestratorType": orch_type,
        }
        if extra_inputs:
            inputs.update(extra_inputs)
        return self.deploy(
            "new_database", inputs,
            poll_interval=poll_interval, timeout=timeout, on_status=on_status,
        )

    def deploy_app(
        self,
        app_name: str,
        namespace: str,
        *,
        orch_type: str = "innershift",
        components: list[dict] | None = None,
        extra_inputs: dict | None = None,
        poll_interval: int = 10,
        timeout: int = 600,
        on_status: Any = None,
    ) -> dict:
        """Deploy a web application end-to-end.

        Returns:
            Dict with scenario, pipeline, and credentials.
        """
        inputs: dict[str, Any] = {
            "applicationName": app_name,
            "namespace": namespace,
            "orchestratorType": orch_type,
        }
        if components:
            inputs["components"] = components
        if extra_inputs:
            inputs.update(extra_inputs)
        return self.deploy(
            "new_web_app", inputs,
            poll_interval=poll_interval, timeout=timeout, on_status=on_status,
        )
