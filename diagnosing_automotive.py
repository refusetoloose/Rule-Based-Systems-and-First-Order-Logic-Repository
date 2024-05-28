# %%
from durable.lang import *


with ruleset("diagnosing_automotive"):

    @when_all((m.engine_gets_gas == True) & (m.engine_turns_over == True))
    def problem_is_spark_plugs(c):
        print(c.m)
        print("The problem is spark plugs.")

    # problem_is_battery_or_cables ?
    @when_all((m.engine_turns_over == False) & (m.lights_come_on == False))
    def problem_is_battery_or_cables(c):
        print(c.m)
        print("The problem is the battery or cables, Check the battery or cables")
    
    # problem_is_starter_motor ?
    @when_all((m.engine_turns_over == False) & (m.lights_come_on == True))
    def problem_is_starter_motor(c):
        print(c.m)
        print("The problem is the starter motor. Check the starter motor")

    # post an event for engine is getting gas?
    @when_all((m.gas_in_fuel_tank == True) & (m.gas_in_carburetor == True))
    def engine_gets_gas(c):
        post("diagnosing_automotive", {"engine_gets_gas" : True})

    # what rule is missing to make this comprehensive?
    # No Fuel
    @when_all((m.gas_in_fuel_tank == False) | (m.gas_in_carburetor == False))
    def engine_gets_no_gas(c):
        print(c.m)
        print("No gas in Car. Please fill Gas.")

    # Problem with fuel system.
    @when_all((m.gas_in_fuel_tank == True) & (m.gas_in_carburetor == False))
    def problem_is_fuel_system_issue(c):
        print(c.m)
        print("The problem might be with the fuel system. Check the fuel pump for blockage or working condition.")

    # Problem with electrical system.
    @when_all((m.engine_turns_over == False) &  (m.lights_come_on == False))
    def electrical_system_issue(c):
        print(c.m)
        print("Electrical system issue. Check battery and fuses.")

    # handle unknown situation?
    @when_all((m.engine_gets_gas == False) & (m.engine_turns_over == False) &
              (m.lights_come_on == False) & (m.gas_in_fuel_tank == False) &
              (m.gas_in_carburetor == False))
    def handle_unknown_situation(c):
        print(c.m)
        print("The situation is unknown. Further diagnostics are required.")

# %%
from itertools import product

for (
    engine_turns_over,
    engine_gets_gas,
    lights_come_on,
    gas_in_fuel_tank,
    gas_in_carburetor,
) in product([True, False], [True, False], [True, False], [True, False], [True, False]):
    fact = {
        "engine_turns_over": engine_turns_over,
        "engine_gets_gas": engine_gets_gas,
        "lights_come_on": lights_come_on,
        "gas_in_fuel_tank": gas_in_fuel_tank,
        "gas_in_carburetor": gas_in_carburetor,
    }
    post("diagnosing_automotive", fact)

# %%
