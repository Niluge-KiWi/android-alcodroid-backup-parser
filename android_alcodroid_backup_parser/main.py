from caterpillar.shortcuts import struct, BigEndian, this, unpack_file
from caterpillar.fields import *

from rich import print
import rich_click as click


_package_name = b"org.M.alcodroid"

@struct(order=BigEndian)
class AllDataAlcoDroidBackup:
    # java DataOutput.writeInt
    version: int32
    # java DataOutput.writeLong
    date: int64
    # java DataOutput.writeUTF: 2 bytes length, then java modified UTF-8
    package_name_lenght: Const(len(_package_name), uint16) # b"\x00\x0f"
    package_name: _package_name # ~magic string
    # java DataOutput.writeUTF: 2 bytes length, then java modified UTF-8
    # TODO parse java modified UTF-8: https://docs.oracle.com/javase/8/docs/api/java/io/DataInput.html#modified-utf-8
    application_name: Prefixed(int16)
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
