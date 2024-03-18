from caterpillar.model import struct
from caterpillar.fields import *

from rich import print
import rich_click as click



@struct
class AllDataAlcoDroidBackup:
    version: int32
    date: int64
    package_name: b"org.M.alcodroid\x00"
    application_name: CString()
    todo: Pass

@struct
class Settings:
    todo: Pass


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def parse(input_path):
    """Parse AlcoDroid all_data.backup file"""

    print(unpack_file(AllDataAlcoDroidBackup, input_path))

if __name__ == '__main__':
    parse()
