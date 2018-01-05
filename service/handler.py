import click

from data import hospital, doctor
from clearing import cleanHospital


@click.group()
def clis():
    pass

clis.add_command(hospital)
clis.add_command(doctor)
clis.add_command(cleanHospital)

if __name__ == "__main__":
    clis()
