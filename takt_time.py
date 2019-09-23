#!/usr/bin/env python

"""Module to calculate takt time of an assembly"""

__author__ = "Michael Tucker"
__copyright__ = "Copyright 2019, Michael Tucker"
__license__ = "GNU v3.0"
__version__ = "1.0.1"
__email__ = "mic.tuc@me.com"


def top_takt_time(top_assy_per_year, weeks_per_year, days_per_week, shifts_per_day, hours_per_shift, roll_thru_yield, line_uptime):
    hours_per_year = hours_per_shift * shifts_per_day * days_per_week * weeks_per_year
    time_availability = hours_per_year / (24 * 365)
    efficiency = roll_thru_yield * time_availability * line_uptime
    top_assy_takt_time = (24 * 365) * efficiency / top_assy_per_year

    return [time_availability, efficiency, top_assy_takt_time]

def sub_assy_takt_time(top_assy_takt_time):
    # Inputs
    units_per_top_assy = 4
    service_units = 1
    roll_thru_yield = 0.98
    sub_takt_time = roll_thru_yield * top_assy_takt_time / (units_per_top_assy + service_units)
    print(sub_takt_time)

def main():
    # Inputs
    top_assy_per_year = 100 # How many top level assemblies are needed each year
    weeks_per_year = 50     # How many weeks per year of production time
    days_per_week = 5       # How many days per week of production time
    shifts_per_day = 1      # How many work shifts per day of production
    hours_per_shift = 7.8   # Effective hours per shift
    roll_thru_yield = 0.98  # Rolled Throughput Yield (RTY), 1-scrap rate
    line_uptime = 0.75      # Percentage of working time when line is running

    [time_availability, efficiency, top_assy_takt_time] = top_takt_time(top_assy_per_year, weeks_per_year, days_per_week, shifts_per_day, hours_per_shift, roll_thru_yield, line_uptime)
    sub_assy_takt_time(top_assy_takt_time)

    print(time_availability)
    print(efficiency)
    print(top_assy_takt_time)

main()
