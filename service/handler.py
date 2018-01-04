import click

from data import hospital, doctor


@click.group()
def clis():
    pass

clis.add_command(hospital)
clis.add_command(doctor)

if __name__ == "__main__":
    clis()
