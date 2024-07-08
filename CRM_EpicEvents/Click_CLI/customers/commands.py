import click
from Click_CLI.customers.link_api import create_customer, \
    delete_customer, update_customer, list_all_customer, list_one_customer
from Click_CLI.constants import NULL_VALUE


@click.group()
def customers():
    pass


@customers.command()
@click.option("--information", prompt="New information", help="...")
@click.option("--full_name", prompt="New full_name", help="...")
@click.option("--email", prompt="New email", help="...")
@click.option("--phone_number", prompt="New phone_number", help="...")
@click.option("--enterprise_name", prompt="New enterprise_name", help="...")
@click.option("--commercial_contact", prompt="New commercial_contact", help="...")
@click.pass_context
def create(ctx, information, full_name, email, phone_number, enterprise_name, commercial_contact):
    click.echo(f"Creating customer {email}")
    ret, resume = create_customer(
        ctx.obj["TOKEN"], information, full_name, email, phone_number, enterprise_name, commercial_contact
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@customers.command()
@click.option("--pk", prompt="Customer id to delete", help="...")
@click.pass_context
def delete(ctx, pk):
    click.echo(f"Deleting customer {pk}")
    ret, resume = delete_customer(ctx.obj["TOKEN"], pk)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@customers.command()
@click.option("--pk", prompt="Customer id to update", help="...")
@click.option(
    "--information",
    prompt="information (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--full_name",
    prompt="full_name (leave blank if you don't want to change)",
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
    "--phone_number",
    prompt="phone_number (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--enterprise_name",
    prompt="enterprise_name (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--commercial_contact",
    prompt="commercial_contact (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.pass_context
def update(ctx, pk, information, full_name, email, phone_number, enterprise_name, commercial_contact):
    click.echo(f"update {pk}")
    ret, resume = update_customer(
        ctx.obj["TOKEN"], pk, information, full_name, email, phone_number, enterprise_name, commercial_contact
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@customers.command()
@click.pass_context
def list_all(ctx):
    ret, resume = list_all_customer(ctx.obj["TOKEN"])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@customers.command()
@click.option("--customer_id", prompt="Customer id to view", help="...")
@click.pass_context
def list_one(ctx, customer_id):
    click.echo(f"viewing customer {customer_id}")
    ret, resume = list_one_customer(ctx.obj["TOKEN"], customer_id)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


"""
@users.command()
@click.pass_context
def refresh(ctx):
    ret, resume = refresh_customer(ctx.obj['REFRESH'])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")
"""
