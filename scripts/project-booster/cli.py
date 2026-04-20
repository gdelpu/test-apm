#!/usr/bin/env python3
"""Project Booster CLI — create environments and CI/CD pipelines.

Usage:
    python -m project_booster <command> [options]

Commands:
    init           Create a .project-booster.json config file
    whoami         Show current authenticated user
    logout         Clear cached user data
    config         Show API config (scenario types, etc.)

    # Profile
    profile show          Show user profile
    profile update        Update user profile

    # Secrets
    secrets list             List stored secrets
    secrets create           Store a new secret
    secrets delete <id>      Delete a secret

    # Trusted certificates
    certs list               List trusted certificates
    certs add                Add a trusted certificate (PEM)
    certs delete <id>        Delete a trusted certificate

    # Scenarios
    scenarios list           List your scenarios
    scenarios create         Create a new scenario
    scenarios get <id>       Show scenario details
    scenarios update <id>    Update a scenario
    scenarios archive <id>   Archive a scenario
    scenarios unarchive <id> Unarchive a scenario
    scenarios delete <id>    Delete a scenario
    scenarios duplicate <id> Duplicate a scenario
    scenarios children <id>  Show child scenarios

    # Pipelines (CI/CD)
    pipeline run <id>        Trigger a pipeline for a scenario
    pipeline status <id>     Get pipeline status & logs
    pipeline wait <id>       Wait for pipeline completion
    pipeline cancel <id>     Cancel a running pipeline
    pipeline creds <id>      Show pipeline credentials

    # Environments (orchestrators)
    env check <type>                    Check orchestrator connection
    env namespaces <type>               List namespaces
    env resources <type>                List namespaces with deployed resources
    env test-create <type> <name>       Test if namespace can be created
    env test-write <type> <name>        Test if namespace is writable
    env services <type> <namespace>     List services in a namespace
    env service <type> <ns> <release>   Get a specific service
    env details <type> <namespace>      Get namespace details
    env role-binding <type> <ns>        Create role binding
    env quotas <type> <ns>              Set namespace quotas

    # Artifactory
    artifactory repos                   List repositories
    artifactory create-repos            Create repositories

    # Certificates (server-side)
    certificates <url>                  List SSL certificates for a URL

    # Admin
    admin config reload                 Reload configuration
    admin config reset                  Reset & reload configuration
    admin banners list                  List banners
    admin banners create                Create a banner
    admin metrics connections           Connection metrics
    admin metrics usage                 Usage metrics
    admin metrics ratings               User ratings
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .config import BoosterConfig, load_config, init_config, DEFAULT_BASE_URL
from .booster_client import BoosterClient, BoosterAPIError, UntrustedCertificateError


def _json_out(data: Any) -> None:
    """Pretty-print JSON to stdout."""
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _make_client(args: argparse.Namespace) -> BoosterClient:
    config = load_config(getattr(args, "config", None))
    return BoosterClient(config)


# ── init ──────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> None:
    base_url = args.url or DEFAULT_BASE_URL
    token = args.token
    if not token:
        token = input("GitLab private token (glpat-…): ").strip()
    path = init_config(base_url, token, ssl_verify=not args.no_ssl_verify)
    print(f"Config written to {path}")


# ── whoami ────────────────────────────────────────────────────────────

def cmd_whoami(args: argparse.Namespace) -> None:
    client = _make_client(args)
    _json_out(client.get_current_user())


# ── logout ────────────────────────────────────────────────────────────

def cmd_logout(args: argparse.Namespace) -> None:
    client = _make_client(args)
    client.logout()
    print("Logged out.", file=sys.stderr)


# ── config (show) ────────────────────────────────────────────────────

def cmd_config(args: argparse.Namespace) -> None:
    client = _make_client(args)
    sub = getattr(args, "sub", None)
    if sub == "auth":
        _json_out(client.get_auth_config())
    else:
        _json_out(client.get_config())


# ── profile ───────────────────────────────────────────────────────────

def cmd_profile(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "show":
        _json_out(client.get_profile())
    elif action == "update":
        profile = json.loads(args.data)
        _json_out(client.update_profile(profile))
        print("Profile updated.", file=sys.stderr)


# ── secrets ───────────────────────────────────────────────────────────

def cmd_secrets(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "list":
        _json_out(client.list_secrets())
    elif action == "create":
        result = client.create_secret(
            key=args.key, value=args.value, secret_type=args.type, label=args.label
        )
        _json_out(result)
        print("Secret created.", file=sys.stderr)
    elif action == "delete":
        client.delete_secret(args.id)
        print(f"Secret {args.id} deleted.", file=sys.stderr)


# ── trusted certificates ─────────────────────────────────────────────

def cmd_certs(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "list":
        _json_out(client.list_trusted_certificates(page=args.page, size=args.size))
    elif action == "add":
        if args.pem_file:
            with open(args.pem_file, encoding="utf-8") as fh:
                pem = fh.read()
        else:
            pem = args.pem
        result = client.add_trusted_certificate(pem)
        _json_out(result)
        print("Certificate added.", file=sys.stderr)
    elif action == "delete":
        client.delete_trusted_certificate(args.id)
        print(f"Certificate {args.id} deleted.", file=sys.stderr)


# ── scenarios ─────────────────────────────────────────────────────────

def cmd_scenarios(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "list":
        result = client.list_scenarios(
            page=args.page, size=args.size, archived=args.archived
        )
        _json_out(result)

    elif action == "create":
        inputs = json.loads(args.inputs) if args.inputs else None
        result = client.create_scenario(
            scenario_type=args.type, version=args.version, inputs=inputs
        )
        _json_out(result)
        print("Scenario created.", file=sys.stderr)

    elif action == "get":
        _json_out(client.get_scenario(args.id))

    elif action == "update":
        inputs = json.loads(args.inputs) if args.inputs else None
        result = client.update_scenario(
            scenario_id=args.id, scenario_type=args.type,
            version=args.version, inputs=inputs,
        )
        _json_out(result)

    elif action == "archive":
        result = client.patch_scenario(args.id, archived=True)
        _json_out(result)
        print(f"Scenario {args.id} archived.", file=sys.stderr)

    elif action == "unarchive":
        result = client.patch_scenario(args.id, archived=False)
        _json_out(result)
        print(f"Scenario {args.id} unarchived.", file=sys.stderr)

    elif action == "delete":
        client.delete_scenario(args.id)
        print(f"Scenario {args.id} deleted.", file=sys.stderr)

    elif action == "children":
        _json_out(client.get_scenario_children(args.id))

    elif action == "duplicate":
        result = client.duplicate_scenario(args.id)
        _json_out(result)
        print("Scenario duplicated.", file=sys.stderr)


# ── pipelines ─────────────────────────────────────────────────────────

def cmd_pipeline(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "run":
        result = client.create_pipeline(
            args.id, skip_previously_failed=args.skip_failed
        )
        _json_out(result)
        print(f"Pipeline triggered for scenario {args.id}.", file=sys.stderr)

    elif action == "status":
        pipeline = client.get_pipeline(args.id)
        _json_out(pipeline)

    elif action == "wait":
        print(
            f"Waiting for pipeline (scenario {args.id}), "
            f"polling every {args.interval}s, timeout {args.timeout}s …",
            file=sys.stderr,
        )
        pipeline = client.wait_for_pipeline(
            args.id, poll_interval=args.interval, timeout=args.timeout
        )
        _json_out(pipeline)
        status = pipeline.get("status", "UNKNOWN")
        print(f"Pipeline finished with status: {status}", file=sys.stderr)
        if status == "FAILED":
            sys.exit(1)

    elif action == "cancel":
        client.cancel_pipeline(args.id)
        print(f"Pipeline for scenario {args.id} cancelled.", file=sys.stderr)

    elif action == "creds":
        _json_out(client.get_pipeline_credentials(args.id))


# ── environments ──────────────────────────────────────────────────────

def cmd_env(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action
    orch_url = getattr(args, "orch_url", None)
    ssl_no = getattr(args, "ssl_no_verify", False)

    if action == "check":
        _json_out(client.check_orchestrator(args.type, url=orch_url, ssl_no_verify=ssl_no))

    elif action == "namespaces":
        _json_out(
            client.list_namespaces(
                args.type,
                url=orch_url,
                page=args.page,
                size=args.size,
                ssl_no_verify=ssl_no,
                full_description=args.full,
                role_bindings=args.role_bindings,
            )
        )

    elif action == "resources":
        _json_out(
            client.list_namespaces_resources(
                args.type, url=orch_url, page=args.page, size=args.size,
                ssl_no_verify=ssl_no,
            )
        )

    elif action == "test-create":
        _json_out(
            client.test_namespace_creation(
                args.type, args.name, url=orch_url, ssl_no_verify=ssl_no
            )
        )

    elif action == "test-write":
        _json_out(
            client.test_namespace_writable(
                args.type, args.name, url=orch_url, ssl_no_verify=ssl_no
            )
        )

    elif action == "services":
        _json_out(
            client.list_namespace_services(
                args.type, args.namespace, url=orch_url,
                page=args.page, size=args.size, ssl_no_verify=ssl_no,
            )
        )

    elif action == "service":
        _json_out(
            client.get_service(
                args.type, args.namespace, args.release,
                url=orch_url, ssl_no_verify=ssl_no,
            )
        )

    elif action == "details":
        _json_out(
            client.get_namespace_details(
                args.type, args.namespace, url=orch_url, ssl_no_verify=ssl_no
            )
        )

    elif action == "role-binding":
        body = json.loads(args.body)
        _json_out(
            client.create_role_binding(
                args.type, args.namespace, body, url=orch_url, ssl_no_verify=ssl_no
            )
        )

    elif action == "quotas":
        body = json.loads(args.body)
        _json_out(
            client.create_quotas(
                args.type, args.namespace, body, url=orch_url, ssl_no_verify=ssl_no
            )
        )


# ── artifactory ───────────────────────────────────────────────────────

def cmd_artifactory(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "repos":
        _json_out(
            client.list_artifactory_repos(
                url=getattr(args, "url", None),
                repo_type=getattr(args, "type", None),
                package_type=getattr(args, "package_type", None),
                page=args.page,
                size=args.size,
            )
        )
    elif action == "create-repos":
        body = json.loads(args.body)
        _json_out(
            client.create_artifactory_repos(
                body,
                url=getattr(args, "url", None),
                package_type=getattr(args, "package_type", None),
            )
        )


# ── certificates ──────────────────────────────────────────────────────

def cmd_certificates(args: argparse.Namespace) -> None:
    client = _make_client(args)
    _json_out(client.list_certificates(args.url))


# ── admin ─────────────────────────────────────────────────────────────

def cmd_admin(args: argparse.Namespace) -> None:
    client = _make_client(args)
    section = args.section
    action = args.action

    if section == "config":
        if action == "reload":
            branch = getattr(args, "branch", None)
            result = client.reload_config(branch=branch)
            _json_out(result)
            print("Configuration reloaded.", file=sys.stderr)
        elif action == "reset":
            client.reset_config()
            print("Configuration reset.", file=sys.stderr)

    elif section == "banners":
        if action == "list":
            _json_out(client.list_banners())
        elif action == "create":
            body = json.loads(args.body)
            result = client.create_banner(body)
            _json_out(result)
            print("Banner created.", file=sys.stderr)

    elif section == "metrics":
        if action == "connections":
            _json_out(client.get_connection_metrics(page=args.page, size=args.size))
        elif action == "usage":
            _json_out(client.get_usage_metrics())
        elif action == "ratings":
            _json_out(client.get_rating_metrics(page=args.page, size=args.size))


# ── scenario-types ────────────────────────────────────────────────────

def cmd_scenario_types(args: argparse.Namespace) -> None:
    client = _make_client(args)
    types = client.get_scenario_types()
    if isinstance(types, dict) and not args.raw:
        # Pretty display
        for key, desc in types.items():
            print(f"  {key:45s} {desc}")
    else:
        _json_out(types)


# ── deploy (end-to-end) ──────────────────────────────────────────────

def _status_printer(pipeline: dict) -> None:
    """Callback for deploy commands — prints pipeline progress."""
    status = pipeline.get("status", "?")
    actions = pipeline.get("actions", [])
    done = sum(1 for a in actions if a.get("status", "").upper() in ("COMPLETED", "SKIPPED"))
    total = len(actions)
    print(f"\r  Pipeline: {status}  [{done}/{total} actions]", end="", file=sys.stderr)


def cmd_deploy(args: argparse.Namespace) -> None:
    client = _make_client(args)
    action = args.action

    if action == "run":
        inputs = json.loads(args.inputs)
        print(f"Deploying scenario type '{args.type}' …", file=sys.stderr)
        result = client.deploy(
            args.type, inputs,
            version=getattr(args, "version", None),
            skip_previously_failed=getattr(args, "skip_failed", False),
            poll_interval=args.interval,
            timeout=args.timeout,
            on_status=_status_printer,
        )
        print(file=sys.stderr)  # newline after progress
        _json_out(result)
        status = result["pipeline"].get("status", "UNKNOWN")
        print(f"Deploy finished: {status}", file=sys.stderr)
        if status == "FAILED":
            sys.exit(1)

    elif action == "db":
        print(
            f"Deploying {args.db_type} database in namespace '{args.namespace}' "
            f"on {args.orch_type} …",
            file=sys.stderr,
        )
        extra = json.loads(args.extra_inputs) if args.extra_inputs else None
        result = client.deploy_database(
            args.db_type, args.namespace,
            orch_type=args.orch_type,
            extra_inputs=extra,
            poll_interval=args.interval,
            timeout=args.timeout,
            on_status=_status_printer,
        )
        print(file=sys.stderr)
        _json_out(result)
        status = result["pipeline"].get("status", "UNKNOWN")
        print(f"Database deploy finished: {status}", file=sys.stderr)
        if result.get("credentials"):
            print("Credentials returned — see JSON output.", file=sys.stderr)
        if status == "FAILED":
            sys.exit(1)

    elif action == "app":
        components = json.loads(args.components) if args.components else None
        extra = json.loads(args.extra_inputs) if args.extra_inputs else None
        print(
            f"Deploying app '{args.app_name}' in namespace '{args.namespace}' "
            f"on {args.orch_type} …",
            file=sys.stderr,
        )
        result = client.deploy_app(
            args.app_name, args.namespace,
            orch_type=args.orch_type,
            components=components,
            extra_inputs=extra,
            poll_interval=args.interval,
            timeout=args.timeout,
            on_status=_status_printer,
        )
        print(file=sys.stderr)
        _json_out(result)
        status = result["pipeline"].get("status", "UNKNOWN")
        print(f"App deploy finished: {status}", file=sys.stderr)
        if result.get("credentials"):
            print("Credentials returned — see JSON output.", file=sys.stderr)
        if status == "FAILED":
            sys.exit(1)


# ── argument parser ───────────────────────────────────────────────────

def _add_pagination(parser: argparse.ArgumentParser) -> None:
    """Add --page and --size arguments."""
    parser.add_argument("--page", type=int, default=0)
    parser.add_argument("--size", type=int, default=20)


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="project-booster",
        description="Project Booster API CLI — manage environments & CI/CD pipelines",
    )
    root.add_argument("--config", "-c", help="Path to .project-booster.json")
    sub = root.add_subparsers(dest="command", required=True)

    # init
    p = sub.add_parser("init", help="Create config file")
    p.add_argument("--url", help=f"API base URL (default: {DEFAULT_BASE_URL})")
    p.add_argument("--token", "-t", help="GitLab private token")
    p.add_argument(
        "--no-ssl-verify", action="store_true", help="Disable SSL verification"
    )

    # whoami
    sub.add_parser("whoami", help="Show current user")

    # logout
    sub.add_parser("logout", help="Logout / clear cached user data")

    # config
    p = sub.add_parser("config", help="Show API config")
    p.add_argument(
        "--auth", dest="sub", action="store_const", const="auth",
        help="Show OAuth2 authentication config instead",
    )

    # ── profile ───────────────────────────────────────────────────────
    sp = sub.add_parser("profile", help="Manage user profile")
    sp_sub = sp.add_subparsers(dest="action", required=True)
    sp_sub.add_parser("show", help="Show user profile")
    p = sp_sub.add_parser("update", help="Update user profile")
    p.add_argument("--data", required=True, help="JSON profile data")

    # ── secrets ───────────────────────────────────────────────────────
    sp = sub.add_parser("secrets", help="Manage secrets")
    sp_sub = sp.add_subparsers(dest="action", required=True)

    sp_sub.add_parser("list", help="List secrets")

    p = sp_sub.add_parser("create", help="Create a secret")
    p.add_argument("--key", required=True, help="Secret key (URL-based identifier)")
    p.add_argument("--value", required=True, help="Secret value")
    p.add_argument("--type", required=True, help="Secret type (openshift, jfrog, …)")
    p.add_argument("--label", required=True, help="Human-readable label")

    p = sp_sub.add_parser("delete", help="Delete a secret")
    p.add_argument("id", type=int, help="Secret ID")

    # ── trusted certificates ──────────────────────────────────────────
    sp = sub.add_parser("certs", help="Manage trusted certificates")
    sp_sub = sp.add_subparsers(dest="action", required=True)

    p = sp_sub.add_parser("list", help="List trusted certificates")
    _add_pagination(p)

    p = sp_sub.add_parser("add", help="Add a trusted certificate")
    pem_group = p.add_mutually_exclusive_group(required=True)
    pem_group.add_argument("--pem", help="PEM certificate string")
    pem_group.add_argument("--pem-file", help="Path to PEM certificate file")

    p = sp_sub.add_parser("delete", help="Delete a trusted certificate")
    p.add_argument("id", type=int, help="Certificate ID")

    # ── scenarios ─────────────────────────────────────────────────────
    sp = sub.add_parser("scenarios", help="Manage scenarios")
    sp_sub = sp.add_subparsers(dest="action", required=True)

    p = sp_sub.add_parser("list", help="List scenarios")
    _add_pagination(p)
    p.add_argument("--archived", type=bool, default=None)

    p = sp_sub.add_parser("create", help="Create a scenario")
    p.add_argument("--type", required=True, help="Scenario type")
    p.add_argument("--version", help="Scenario version")
    p.add_argument("--inputs", help="JSON string of input parameters")

    p = sp_sub.add_parser("get", help="Get scenario details")
    p.add_argument("id", type=int, help="Scenario ID")

    p = sp_sub.add_parser("update", help="Update scenario")
    p.add_argument("id", type=int, help="Scenario ID")
    p.add_argument("--type", required=True, help="Scenario type")
    p.add_argument("--version", help="Scenario version")
    p.add_argument("--inputs", help="JSON string of input parameters")

    p = sp_sub.add_parser("archive", help="Archive a scenario")
    p.add_argument("id", type=int, help="Scenario ID")

    p = sp_sub.add_parser("unarchive", help="Unarchive a scenario")
    p.add_argument("id", type=int, help="Scenario ID")

    p = sp_sub.add_parser("delete", help="Delete a scenario")
    p.add_argument("id", type=int, help="Scenario ID")

    p = sp_sub.add_parser("duplicate", help="Duplicate a scenario")
    p.add_argument("id", type=int, help="Scenario ID to duplicate")

    p = sp_sub.add_parser("children", help="List child scenarios")
    p.add_argument("id", type=int, help="Parent scenario ID")

    # ── pipeline ──────────────────────────────────────────────────────
    sp = sub.add_parser("pipeline", help="Manage CI/CD pipelines")
    sp_sub = sp.add_subparsers(dest="action", required=True)

    p = sp_sub.add_parser("run", help="Trigger a pipeline")
    p.add_argument("id", type=int, help="Scenario ID")
    p.add_argument(
        "--skip-failed", action="store_true",
        help="Skip previously failed actions",
    )

    p = sp_sub.add_parser("status", help="Get pipeline status")
    p.add_argument("id", type=int, help="Scenario ID")

    p = sp_sub.add_parser("wait", help="Wait for pipeline to finish")
    p.add_argument("id", type=int, help="Scenario ID")
    p.add_argument("--interval", type=int, default=10, help="Poll interval (seconds)")
    p.add_argument("--timeout", type=int, default=600, help="Timeout (seconds)")

    p = sp_sub.add_parser("cancel", help="Cancel a running pipeline")
    p.add_argument("id", type=int, help="Scenario ID")

    p = sp_sub.add_parser("creds", help="Get pipeline credentials")
    p.add_argument("id", type=int, help="Scenario ID")

    # ── env ───────────────────────────────────────────────────────────
    sp = sub.add_parser("env", help="Manage environments (orchestrators)")
    sp.add_argument("--orch-url", help="Orchestrator API URL")
    sp.add_argument("--ssl-no-verify", action="store_true")
    sp_sub = sp.add_subparsers(dest="action", required=True)

    p = sp_sub.add_parser("check", help="Check orchestrator connection")
    p.add_argument("type", help="Orchestrator type (openshift, kubernetes)")

    p = sp_sub.add_parser("namespaces", help="List namespaces")
    p.add_argument("type", help="Orchestrator type")
    _add_pagination(p)
    p.add_argument(
        "--full", action="store_true", default=True,
        help="Include Kasten / sleep info",
    )
    p.add_argument(
        "--role-bindings", action="store_true",
        help="Include role binding details",
    )

    p = sp_sub.add_parser("resources", help="List namespaces with deployed resources")
    p.add_argument("type", help="Orchestrator type")
    _add_pagination(p)

    p = sp_sub.add_parser("test-create", help="Test if namespace can be created")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("name", help="Namespace name")

    p = sp_sub.add_parser("test-write", help="Test if namespace is writable")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("name", help="Namespace name")

    p = sp_sub.add_parser("services", help="List services in a namespace")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("namespace", help="Namespace name")
    _add_pagination(p)

    p = sp_sub.add_parser("service", help="Get a specific deployed service")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("namespace", help="Namespace name")
    p.add_argument("release", help="Helm release name")

    p = sp_sub.add_parser("details", help="Get namespace details")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("namespace", help="Namespace name")

    p = sp_sub.add_parser("role-binding", help="Create a role binding")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("namespace", help="Namespace name")
    p.add_argument("--body", required=True, help="JSON body for the role binding")

    p = sp_sub.add_parser("quotas", help="Set namespace quotas")
    p.add_argument("type", help="Orchestrator type")
    p.add_argument("namespace", help="Namespace name")
    p.add_argument("--body", required=True, help="JSON body for the quotas")

    # ── artifactory ───────────────────────────────────────────────────
    sp = sub.add_parser("artifactory", help="Manage Artifactory repositories")
    sp_sub = sp.add_subparsers(dest="action", required=True)

    p = sp_sub.add_parser("repos", help="List repositories")
    p.add_argument("--url", help="Artifactory URL")
    p.add_argument("--type", help="Repository type")
    p.add_argument("--package-type", help="Package type filter")
    _add_pagination(p)

    p = sp_sub.add_parser("create-repos", help="Create repositories")
    p.add_argument("--body", required=True, help="JSON body for repository creation")
    p.add_argument("--url", help="Artifactory URL")
    p.add_argument("--package-type", help="Package type")

    # ── certificates ──────────────────────────────────────────────────
    p = sub.add_parser("certificates", help="List SSL certificates for a URL")
    p.add_argument("url", help="Target URL to inspect certificates")

    # ── scenario-types ────────────────────────────────────────────────
    p = sub.add_parser("scenario-types", help="List available scenario types")
    p.add_argument("--raw", action="store_true", help="Output raw JSON from /api/config")

    # ── deploy (end-to-end convenience) ───────────────────────────────
    sp = sub.add_parser(
        "deploy",
        help="End-to-end deploy: create scenario → pipeline → wait → credentials",
    )
    sp_sub = sp.add_subparsers(dest="action", required=True)

    # deploy run (generic)
    p = sp_sub.add_parser("run", help="Deploy any scenario type end-to-end")
    p.add_argument("--type", required=True, help="Scenario type (use 'scenario-types' to list)")
    p.add_argument("--inputs", required=True, help="JSON string of scenario inputs")
    p.add_argument("--version", help="Scenario version")
    p.add_argument("--skip-failed", action="store_true", help="Skip previously failed actions")
    p.add_argument("--interval", type=int, default=10, help="Poll interval in seconds")
    p.add_argument("--timeout", type=int, default=600, help="Max wait in seconds")

    # deploy db (database shortcut)
    p = sp_sub.add_parser("db", help="Deploy a database (postgresql, mysql, mongodb, elasticsearch)")
    p.add_argument("db_type", choices=["postgresql", "mysql", "mongodb", "elasticsearch"],
                   help="Database engine")
    p.add_argument("namespace", help="Target namespace")
    p.add_argument("--orch-type", default="innershift",
                   help="Orchestrator type (default: innershift)")
    p.add_argument("--extra-inputs", help="Additional JSON inputs to merge")
    p.add_argument("--interval", type=int, default=10, help="Poll interval in seconds")
    p.add_argument("--timeout", type=int, default=600, help="Max wait in seconds")

    # deploy app (web application shortcut)
    p = sp_sub.add_parser("app", help="Deploy a web application end-to-end")
    p.add_argument("app_name", help="Application name")
    p.add_argument("namespace", help="Target namespace")
    p.add_argument("--orch-type", default="innershift",
                   help="Orchestrator type (default: innershift)")
    p.add_argument("--components", help="JSON array of component definitions")
    p.add_argument("--extra-inputs", help="Additional JSON inputs to merge")
    p.add_argument("--interval", type=int, default=10, help="Poll interval in seconds")
    p.add_argument("--timeout", type=int, default=600, help="Max wait in seconds")

    # ── admin ─────────────────────────────────────────────────────────
    sp = sub.add_parser("admin", help="Admin operations")
    sp_sub = sp.add_subparsers(dest="section", required=True)

    # admin config
    adm_config = sp_sub.add_parser("config", help="Admin config operations")
    adm_config_sub = adm_config.add_subparsers(dest="action", required=True)
    p = adm_config_sub.add_parser("reload", help="Reload configuration")
    p.add_argument("--branch", help="Git branch to reload from")
    adm_config_sub.add_parser("reset", help="Reset & reload configuration")

    # admin banners
    adm_banners = sp_sub.add_parser("banners", help="Manage banners")
    adm_banners_sub = adm_banners.add_subparsers(dest="action", required=True)
    adm_banners_sub.add_parser("list", help="List banners")
    p = adm_banners_sub.add_parser("create", help="Create a banner")
    p.add_argument("--body", required=True, help="JSON body for the banner")

    # admin metrics
    adm_metrics = sp_sub.add_parser("metrics", help="View metrics")
    adm_metrics_sub = adm_metrics.add_subparsers(dest="action", required=True)
    p = adm_metrics_sub.add_parser("connections", help="Connection metrics")
    _add_pagination(p)
    adm_metrics_sub.add_parser("usage", help="Usage metrics")
    p = adm_metrics_sub.add_parser("ratings", help="User ratings")
    _add_pagination(p)

    return root


# ── dispatch ──────────────────────────────────────────────────────────

DISPATCH = {
    "init": cmd_init,
    "whoami": cmd_whoami,
    "logout": cmd_logout,
    "config": cmd_config,
    "profile": cmd_profile,
    "secrets": cmd_secrets,
    "certs": cmd_certs,
    "scenarios": cmd_scenarios,
    "pipeline": cmd_pipeline,
    "env": cmd_env,
    "artifactory": cmd_artifactory,
    "certificates": cmd_certificates,
    "scenario-types": cmd_scenario_types,
    "deploy": cmd_deploy,
    "admin": cmd_admin,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    handler = DISPATCH.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)
    try:
        handler(args)
    except UntrustedCertificateError as exc:
        print(
            "Error: untrusted SSL certificate detected.\n"
            "Trust the certificate with: project-booster certs add --pem-file <cert.pem>\n"
            f"Details: {exc}",
            file=sys.stderr,
        )
        sys.exit(2)
    except BoosterAPIError as exc:
        print(f"API error: {exc}", file=sys.stderr)
        if isinstance(exc.body, dict):
            _json_out(exc.body)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
