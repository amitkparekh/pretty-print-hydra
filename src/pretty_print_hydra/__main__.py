from pathlib import Path
from typing import Annotated, Optional

import hydra
import typer
from rich import print as rich_print

from pretty_print_hydra.hydra import load_hydra_config
from pretty_print_hydra.pretty import pretty_print_config, prettyify_hydra_config, prettyify_inputs

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True, add_completion=False)


@app.command(no_args_is_help=True)
def main(  # noqa: WPS234
    *,
    config_file: Annotated[
        Path, typer.Argument(help="Path to the Hydra config file.", exists=True)
    ],
    overrides: Annotated[
        Optional[list[str]],  # noqa: UP007
        typer.Argument(
            help="Any overrides to apply to the config file.",
            rich_help_panel="Secondary Arguments",
        ),
    ] = None,
    should_instantiate: Annotated[
        bool,
        typer.Option(
            "--instantiate",
            "--init",
            "-i",
            help="Instantiate the given config",
            rich_help_panel="Additional Processing",
        ),
    ] = False,
    preprocess_config_target: Annotated[
        str | None,
        typer.Option(
            "--preprocess-config-target",
            "--preprocess",
            "-p",
            help="Preprocess the config using the given target",
            rich_help_panel="Additional Processing",
            hidden=True,
        ),
    ] = None,
    remove_hydra_key: Annotated[
        bool,
        typer.Option(
            help="Whether the [code]hydra[/code] key should be removed from the config.",
            rich_help_panel="Hydra Options",
        ),
    ] = True,
    hydra_version: Annotated[
        str,
        typer.Option(help="Hydra version to use when parsing.", rich_help_panel="Hydra Options"),
    ] = "1.3",
) -> None:
    """Pretty print Hydra config.

    Instantiating the config just means that the config is instantiated using Hydra's `instantiate`
    function. The values are not kept or stored anywhere and memory is discarded after. This just
    makes sure that the config is valid _and_ can be instantiated without any issues.
    """
    # Step 0. Preprocess the config
    if preprocess_config_target:
        raise NotImplementedError("Preprocessing is not yet implemented.")

    # Step 1. Parse the config
    config = load_hydra_config(
        config_dir=config_file.parent,
        config_file_name=config_file.name,
        overrides=overrides,
        hydra_version_base=hydra_version,
        should_remove_hydra_key_from_config=remove_hydra_key,
    )
    rich_print("[green]:thumbsup: Config Parsed!")

    # Step 2. Instantiate the config if desired
    if should_instantiate:
        _ = hydra.utils.instantiate(config)
        assert _
        rich_print("[green]:thumbsup: Config Instantiated!")

    # Print the configs
    pretty_inputs = prettyify_inputs(config_file, overrides or [])
    pretty_config = prettyify_hydra_config(config)
    pretty_print_config(pretty_inputs, pretty_config)


if __name__ == "__main__":
    app()
