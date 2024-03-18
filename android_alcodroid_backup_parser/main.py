from caterpillar.shortcuts import struct, BigEndian, this, unpack_file
from caterpillar.fields import *

from rich import print
import rich_click as click

from rich.traceback import install
install()

_package_name = b"org.M.alcodroid"



@struct(order=BigEndian)
class Settings:
    # TODO support other versions?
    version: Const(1003, int32)
    volumeUnit: Prefixed(uint16, 'utf8')
    bodyMassUnit: Prefixed(uint16, 'utf8')
    bloodAlcoholUnit: Prefixed(uint16, 'utf8')
    pureAlcoholUnit: Prefixed(uint16, 'utf8')
    alcoholPerTimeUnit: Prefixed(uint16, 'utf8')
    _unknown_f9082f: boolean # no idea yet what it is
    disclaimerAccepted: boolean
    homeTimeZone: Prefixed(uint16, 'utf8') #.getID());
    sexMale: boolean
    bodyMassKg: float64
    consumptionSetpoint: float64
    useConsumptionSetpoint: boolean
    legalLimitPermille: float64
    dayStartMs: int64
    permanentBackupFrequency: Prefixed(uint16, 'utf8')
    bacChartGradient: boolean
    bacChartGridLines: boolean
    bacChartLegalLine: boolean
    numRecentButtons: int32
    adBannerOnTop: boolean
    trackCosts: boolean
    animateTexts: boolean
    bacTextGrow: boolean
    currencySymbol: Prefixed(uint16, 'utf8')
    metabolismRatePointPerCent: float64


@struct(order=BigEndian)
class JournalDrinkEntry:
    # TODO support other versions?
    version: Const(1002, int32)
    name: Prefixed(uint16, 'utf8')
    _unknown_possibly_comment: Prefixed(uint16, 'utf8')
    volume: float64
    alcohol_percentage: float64
    _unknown_some_date_maybe_start_date: int64 #.getTime());
    cost: float64
    _unknown_bool_maybe_set_end_date_equal_to_start_date: boolean
    _unknown_some_date_maybe_end_date: int64
    _unknown_f9452k: boolean
    _unknown_f9465z: int64

@struct(order=BigEndian)
class JournalDrinks:
    # TODO support other versions?
    version: Const(1002, int32)
    creation_date: int64
    size: int32
    entries: JournalDrinkEntry[this.size]

@struct(order=BigEndian)
class DrinksPresets:
    todo: Pass



@struct(order=BigEndian)
class AllDataAlcoDroidBackup:
    # java DataOutput.writeInt
    version: Const(1000, int32)
    # java DataOutput.writeLong
    date: int64
    # java DataOutput.writeUTF: 2 bytes length, then java modified UTF-8
    package_name_lenght: Const(len(_package_name), uint16) # b"\x00\x0f"
    package_name: _package_name # ~magic string
    # java DataOutput.writeUTF: 2 bytes length, then java modified UTF-8
    # TODO parse java modified UTF-8? https://docs.oracle.com/javase/8/docs/api/java/io/DataInput.html#modified-utf-8
    application_name: Prefixed(uint16, 'utf8')
    settings: Settings
    journal_drinks: JournalDrinks
    drinks_presets: DrinksPresets


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def parse(input_path):
    """Parse AlcoDroid all_data.backup file"""

    print(unpack_file(AllDataAlcoDroidBackup, input_path))

if __name__ == '__main__':
    parse()
