# eops/cli.py
import typer
from pathlib import Path
from .utils.config_loader import load_config_from_file
from .core.engine import LiveEngine
from .core.backtester import BacktestEngine

main_app = typer.Typer(help="Eops - A quantitative trading framework.")

@main_app.command()
def run(
    config_file: Path = typer.Argument(..., help="Path to the Python configuration file.", exists=True),
    backtest: bool = typer.Option(False, "--backtest", "-b", help="Run in backtesting mode."),
):
    """
    Run a trading strategy from a configuration file.
    """
    typer.echo(f"🚀 Starting Eops runner...")
    typer.echo(f"⚙️  Config file: {config_file}")

    try:
        config = load_config_from_file(config_file)
        
        if backtest:
            typer.secho("MODE: Backtesting", fg=typer.colors.YELLOW)
            engine = BacktestEngine(config)
            engine.run()
        else:
            typer.secho("MODE: Live Trading", fg=typer.colors.GREEN)
            engine = LiveEngine(config)
            engine.run()
            
    except (FileNotFoundError, AttributeError, ImportError, ValueError) as e:
        typer.secho(f"🔥 Error loading configuration: {e}", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"🔥 An unexpected application error occurred: {e}", fg=typer.colors.RED)


@main_app.command()
def info():
    """Displays information about eops."""
    from . import __version__
    typer.echo(f"Eops Quant Trading Library v{__version__}")

if __name__ == "__main__":
    main_app()