from caterpillar.shortcuts import struct, BigEndian, this, unpack_file
from caterpillar.fields import *

import json
import jsonlines

from rich import print
import rich_click as click

from rich.traceback import install
install()

_package_name = b"org.M.alcodroid"


import types


from typing import Any
import datetime

from caterpillar.abc import _ContextLike

# indirect types
class DateField(PyStructFormattedField):
    """int64 storing millisecond timestamp"""
    def __init__(self) -> None:
        # int64 initialization
        super(DateField, self).__init__('q', datetime.datetime)

    def unpack_single(self, context: _ContextLike) -> Any:
        value = super(DateField, self).unpack_single(context)
        if value is None or 0:
            # 0 is when date not set
            return None

        return datetime.datetime.fromtimestamp(value/1000)

# TODO use DateField for fancy print
#date = DateField()
date = int64 # timestamp: ms since epoch

#TODO duration ms type too?


@struct(order=BigEndian)
class Settings:
    # TODO support other versions?
    version: Const(1003, int32)
    volumeUnit: Prefixed(uint16, encoding='utf8')
    bodyMassUnit: Prefixed(uint16, encoding='utf8')
    bloodAlcoholUnit: Prefixed(uint16, encoding='utf8')
    pureAlcoholUnit: Prefixed(uint16, encoding='utf8')
    alcoholPerTimeUnit: Prefixed(uint16, encoding='utf8')
    show_body_settings: boolean # probably
    disclaimerAccepted: boolean
    homeTimeZone: Prefixed(uint16, encoding='utf8') # TimeZone.getID()); // e.g. "Europe/Paris"
    sexMale: boolean
    bodyMassKg: float64
    consumptionSetpoint: float64
    useConsumptionSetpoint: boolean
    legalLimitPermille: float64
    dayStartMs: int64
    permanentBackupFrequency: Prefixed(uint16, encoding='utf8')
    bacChartGradient: boolean
    bacChartGridLines: boolean
    bacChartLegalLine: boolean
    numRecentButtons: int32
    adBannerOnTop: boolean
    trackCosts: boolean
    animateTexts: boolean
    bacTextGrow: boolean
    currencySymbol: Prefixed(uint16, encoding='utf8')
    metabolismRatePointPerCent: float64


@struct(order=BigEndian)
class JournalDrinkEntry:
    # TODO support other versions?
    version: Const(1002, int32)
    name: Prefixed(uint16, encoding='utf8')
    comment: Prefixed(uint16, encoding='utf8') # probably, always empty
    volume: float64
    alcohol_percentage: float64
    start_date: date
    cost: float64
    input_time_advanced: boolean
    end_date: date
    show_finish_drink_button_in_main_screen: boolean
    absorption_lag_time: int64 # ms

@struct(order=BigEndian)
class JournalDrinks:
    # TODO support other versions?
    version: Const(1002, int32)
    creation_date: date
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
    date: date
    # java DataOutput.writeUTF: 2 bytes length, then java modified UTF-8
    package_name_lenght: Const(len(_package_name), uint16) # b"\x00\x0f"
    package_name: _package_name # ~magic string
    # java DataOutput.writeUTF: 2 bytes length, then java modified UTF-8
    # TODO parse java modified UTF-8? https://docs.oracle.com/javase/8/docs/api/java/io/DataInput.html#modified-utf-8
    application_name: Prefixed(uint16, encoding='utf8')
    settings: Settings
    journal_drinks: JournalDrinks
    drinks_presets: DrinksPresets


def parse(input_path):
    """Parse AlcoDroid all_data.backup file"""
    return unpack_file(AllDataAlcoDroidBackup, input_path)


@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
def show(input_path):
    """Parse and show AlcoDroid all_data.backup file"""
    all_data = parse(input_path)

    print(all_data)

@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('-f', '--format',
              default='jsonl',
              type=click.Choice(['json', 'jsonl']),
              help='output format')
def extract_entries(input_path, output_path, format):
    """Parse AlcoDroid all_data.backup file an extract its journal entries into output jsonlines file"""
    all_data = parse(input_path)

    if format == 'jsonl':
        with jsonlines.open(output_path, mode='w') as writer:
            for entry in all_data.journal_drinks.entries:
                writer.write(entry.__dict__)
    elif format == 'json':
        with open(output_path, mode='w') as f:
            json.dump([entry.__dict__ for entry in all_data.journal_drinks.entries], f)

    click.echo(f"Wrote {format} journal entries to {output_path}")


if __name__ == '__main__':
    cli()
