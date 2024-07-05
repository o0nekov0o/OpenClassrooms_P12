import click
from Click_CLI.events.link_api import create_events, delete_events, \
    update_events, list_all_events, list_one_event
from Click_CLI.constants import NULL_VALUE


@click.group()
def events():
    pass


@events.command()
@click.option("--contract", prompt="New contract", help="...")
@click.option("--event_start_date", prompt="New event_start_date", help="...")
@click.option("--event_end_date", prompt="New event_end_date", help="...")
@click.option("--support_contact", prompt="New support_contact", help="...")
@click.option("--attendees", prompt="New attendees", help="...")
@click.option("--location", prompt="New location", help="...")
@click.option("--notes", prompt="New notes", help="...")
@click.pass_context
def create(ctx, contract, event_start_date, event_end_date, support_contact, attendees, location, notes):
    click.echo(f"Creating event {contract}")
    ret, resume = create_events(
        ctx.obj["TOKEN"], contract, event_start_date, event_end_date, support_contact, attendees, location, notes
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@events.command()
@click.option("--pk", prompt="Event id to delete", help="...")
@click.pass_context
def delete(ctx, pk):
    click.echo(f"Deleting event {pk}")
    ret, resume = delete_events(ctx.obj["TOKEN"], pk)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@events.command()
@click.option("--pk", prompt="Event id to update", help="...")
@click.option(
    "--contract",
    prompt="contract (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--event_start_date",
    prompt="event_start_date (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--event_end_date",
    prompt="event_end_date (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--support_contact",
    prompt="support_contact (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--attendees",
    prompt="attendees (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--location",
    prompt="location (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--notes",
    prompt="notes (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.pass_context
def update(ctx, pk, contract, event_start_date, event_end_date, support_contact, attendees, location, notes):
    click.echo(f"update {pk}")
    ret, resume = update_events(
        ctx.obj["TOKEN"], pk, contract, event_start_date,
        event_end_date, support_contact, attendees, location, notes
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@events.command()
@click.pass_context
def list_all(ctx):
    ret, resume = list_all_events(ctx.obj["TOKEN"])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@events.command()
@click.option("--event_id", prompt="Event id to view", help="...")
@click.pass_context
def list_one(ctx, event_id):
    click.echo(f"viewing event {event_id}")
    ret, resume = list_one_event(ctx.obj["TOKEN"], event_id)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


"""
@users.command()
@click.pass_context
def refresh(ctx):
    ret, resume = refresh_event(ctx.obj['REFRESH'])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")
"""
