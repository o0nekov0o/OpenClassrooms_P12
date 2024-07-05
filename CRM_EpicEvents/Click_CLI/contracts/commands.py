import click
from Click_CLI.contracts.link_api import create_contracts, delete_contracts, \
    update_contracts, list_all_contracts, list_one_contract
from Click_CLI.constants import NULL_VALUE


@click.group()
def contracts():
    pass


@contracts.command()
@click.option("--customer", prompt="New customer", help="...")
@click.option("--total_amount", prompt="New total_amount", help="...")
@click.option("--unpaid_amount", prompt="New unpaid_amount", help="...")
@click.option(
    "--contract_state",
    prompt="New contract_state (0=NOT_SIGNED, 1=SIGNED)",
    type=click.Choice(['0', '1'], case_sensitive=False),
    help="...",
)
@click.pass_context
def create(ctx, customer, total_amount, unpaid_amount, contract_state):
    click.echo(f"Creating contract {customer}")
    ret, resume = create_contracts(
        ctx.obj["TOKEN"], customer, total_amount, unpaid_amount, contract_state
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@contracts.command()
@click.option("--pk", prompt="Contract id to delete", help="...")
@click.pass_context
def delete(ctx, pk):
    click.echo(f"Deleting contract {pk}")
    ret, resume = delete_contracts(ctx.obj["TOKEN"], pk)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@contracts.command()
@click.option("--pk", prompt="Contract id to update", help="...")
@click.option(
    "--customer",
    prompt="customer (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--total_amount",
    prompt="total_amount (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--unpaid_amount",
    prompt="unpaid_amount (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.option(
    "--contract_state",
    prompt="contract_state (leave blank if you don't want to change)",
    default=NULL_VALUE,
    help="...",
)
@click.pass_context
def update(ctx, pk, customer, total_amount, unpaid_amount, contract_state):
    click.echo(f"update {pk}")
    ret, resume = update_contracts(
        ctx.obj["TOKEN"], pk, customer, total_amount, unpaid_amount, contract_state
    )
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@contracts.command()
@click.pass_context
def list_all(ctx):
    ret, resume = list_all_contracts(ctx.obj["TOKEN"])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


@contracts.command()
@click.option("--contract_id", prompt="Contract id to view", help="...")
@click.pass_context
def list_one(ctx, contract_id):
    click.echo(f"viewing contract {contract_id}")
    ret, resume = list_one_contract(ctx.obj["TOKEN"], contract_id)
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")


"""
@users.command()
@click.pass_context
def refresh(ctx):
    ret, resume = refresh_contract(ctx.obj['REFRESH'])
    click.echo(f"return code {ret}")
    click.echo(f"resume {resume}")
"""
