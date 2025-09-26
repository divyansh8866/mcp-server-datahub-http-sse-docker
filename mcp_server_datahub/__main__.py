import logging
from typing import Optional

import click
from datahub.ingestion.graph.config import ClientMode
from datahub.sdk.main_client import DataHubClient
from datahub.telemetry import telemetry
from fastmcp.server.middleware.logging import LoggingMiddleware
from typing_extensions import Literal

from mcp_server_datahub._telemetry import TelemetryMiddleware
from mcp_server_datahub._version import __version__
from mcp_server_datahub.mcp_server import mcp, with_datahub_client

# --- Logging ------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-server-datahub")


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "http"]),
    default="stdio",
    show_default=True,
    help="Transport to use for the MCP server.",
)
@click.option(
    "--host",
    default="0.0.0.0",
    show_default=True,
    help="Host/interface to bind (applies to http/sse).",
)
@click.option(
    "--port",
    type=int,
    default=3001,
    show_default=True,
    help="Port to bind (applies to http/sse).",
)
@click.option(
    "--sse-path",
    default="/sse",
    show_default=True,
    help="SSE endpoint path (applies to sse).",
)
@click.option(
    "--stateless-http/--stateful-http",
    default=True,
    show_default=True,
    help="Run HTTP transport in stateless mode (recommended for simple deployments).",
)
@click.option(
    "--no-banner",
    is_flag=True,
    default=False,
    help="Hide startup banner.",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable verbose request/response logging.",
)
@telemetry.with_telemetry(capture_kwargs=["transport"])
def main(
    transport: Literal["stdio", "sse", "http"],
    host: str,
    port: int,
    sse_path: str,
    stateless_http: bool,
    no_banner: bool,
    debug: bool,
) -> None:
    """
    DataHub MCP server launcher with STDIO/SSE/HTTP transports.
    """
    # DataHub client from env (DATAHUB_GMS_URL, DATAHUB_GMS_TOKEN, etc.)
    client = DataHubClient.from_env(
        client_mode=ClientMode.SDK,
        datahub_component=f"mcp-server-datahub/{__version__}",
    )

    # Middlewares
    if debug:
        logger.setLevel(logging.DEBUG)
        mcp.add_middleware(LoggingMiddleware(include_payloads=True))
    mcp.add_middleware(TelemetryMiddleware())

    # Run server
    with with_datahub_client(client):
        show_banner = not no_banner

        if transport == "stdio":
            mcp.run(transport="stdio", show_banner=show_banner)
            return

        if transport == "http":
            # FastMCP supports stateless HTTP; bind host/port.
            mcp.run(
                transport="http",
                host=host,
                port=port,
                show_banner=show_banner,
                stateless_http=stateless_http,
            )
            return

        if transport == "sse":
            # Expose SSE on /sse by default, bind host/port.
            # (FastMCP accepts sse_path if supported; harmless if ignored.)
            mcp.run(
                transport="sse",
                host=host,
                port=port,
                sse_path=sse_path,
                show_banner=show_banner,
            )
            return


if __name__ == "__main__":
    main()