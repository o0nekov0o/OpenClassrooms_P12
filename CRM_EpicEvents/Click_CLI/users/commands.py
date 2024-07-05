import click
from Click_CLI.users.link_api import create_user, delete_user, update_user, list_all_user, list_one_user
from Click_CLI.constants import NULL_VALUE


@click.group()
def users():
    pass


@users.command()
@click.option("--username", prompt="New username", help="...")
@click.option("--password", prompt="New password", hide_input=True, help="...")
@click.option("--first_name", prompt="New first_name", help="...")
@click.option("--last_name", prompt="New last_name", help="...")
@click.option("--email", prompt="New email", help="...")
@click.option(
    "--collaborator_type",
    prompt="New collaborator_type (0=GES, 1=COM, 2=SUP)",
    type=click.Choice(['0', '1', '2'], case_sensitive=False),
    help="...",
)
@click.pass_context
def create(ctx, username, password, first_name, last_name, email, collaborator_type):
    click.echo(f"Creating user {username}")
    ret, resume = create_user(
        ctx.obj["TOKEN"], username, password, first_name, last_name, email, collaborator_type
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@users.command()
@click.option("--pk", prompt="User id to delete", help="...")
@click.pass_context
def delete(ctx, pk):
    click.echo(f"Deleting user {pk}")
    ret, resume = delete_user(ctx.obj["TOKEN"], pk)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@users.command()
@click.option("--pk", prompt="User id to update", help="...")
@click.option(
    "--username",
    prompt="username (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--password",
    prompt="password (leave blank if you don't want to change)",
    hide_input=True,
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--first_name",
    prompt="first_name (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--last_name",
    prompt="last_name (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--email",
    prompt="email (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--collaborator_type",
    prompt="collaborator_type (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.pass_context
def update(ctx, pk, username, password, first_name, last_name, email, collaborator_type):
    click.echo(f"update {pk}")
    ret, resume = update_user(
        ctx.obj["TOKEN"], pk, username, password, first_name, last_name, email, collaborator_type
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@users.command()
@click.pass_context
def list_all(ctx):
    ret, resume = list_all_user(ctx.obj["TOKEN"])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@users.command()
@click.option("--user_id", prompt="User id to view", help="...")
@click.pass_context
def list_one(ctx, user_id):
    click.echo(f"viewing user {user_id}")
    ret, resume = list_one_user(ctx.obj["TOKEN"], user_id)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


"""
@users.command()
@click.pass_context
def refresh(ctx):
    ret, resume = refresh_user(ctx.obj['REFRESH'])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")
"""
