import numpy as np
import altair as alt

import matplotlib.pyplot as plt

from scipy.stats import norm, binom
from scipy.stats import ttest_1samp
from scipy.stats import ttest_ind

# %%
# declare constants
# calculate the debt cost of capital + customer acquisition costs
SOLAR_PER_KW = 2843 + 6.25

# assume 3.3% interest rate on debt
DEBT_INTEREST_RATE = 0.0345
DSCR_THRESHOLD = 1.25

# potential sensitivity Call Provisions: Callable Bonds
# other initial costs
STARTUP_COSTS = 400000

# %%
# Given values for debt service calculation
loan_term = 25  # 25-year loan


# Formula to calculate annual debt service for a fixed-rate loan
# itc is the investment tax credit flag
def calculate_annual_debt_service(principal, loan_term_years, interest_rate=DEBT_INTEREST_RATE, itc=False):
    if itc:
        principal = principal * 0.7
    r = interest_rate
    n = loan_term_years
    annual_debt_service = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return annual_debt_service


# %%
# calculate startup costs of commercial adoption if 100% of all multifamily buildings in Ann Arbor adopt solar
NUM_APTS = 40
NUM_HOTELS = 40  # ASSUMPTION only 40 hotels in Ann Arbor will participate in the program

TOTAL_COMMERCIAL = NUM_APTS + NUM_HOTELS
# each commercial building will have a 100 kW solar system
COMMERCIAL_SOLAR_PER_KW = 2212
COMMERCIAL_COSTS = TOTAL_COMMERCIAL * COMMERCIAL_SOLAR_PER_KW * 100

# add installation costs for commercial batteries
# assume 60kW * 4-hour battery system at $400/kWh
BATTERY_COST = 400 * 60 * 4 * TOTAL_COMMERCIAL
# add installation costs for commercial solar
COMMERCIAL_COSTS += BATTERY_COST

# %%
# plot annual debt service of solar generation as a function of solar capacity
solar_capacities = np.linspace(10000, 100000, 1000)

# create a list of potential solar generation upfront costs
solar_generation_costs = [SOLAR_PER_KW * solar_capacities + STARTUP_COSTS,
                          SOLAR_PER_KW * solar_capacities + STARTUP_COSTS + COMMERCIAL_COSTS]

# apply the debt service formula to each solar generation cost
debt_services = []
for cost in solar_generation_costs:
    # add variable costs to the debt service
    # 500000 for operator costs per year, 100 for IT costs per year
    OPERATION_COSTS = 500100

    debt_services.append(
        calculate_annual_debt_service(cost, 15, itc=True) + OPERATION_COSTS)
    debt_services.append(
        calculate_annual_debt_service(cost, 25, itc=True) + OPERATION_COSTS)
    debt_services.append(
        calculate_annual_debt_service(cost, 30, itc=True) + OPERATION_COSTS)
    debt_services.append(
        calculate_annual_debt_service(cost, 15, itc=True, interest_rate=0.04) + OPERATION_COSTS)
    debt_services.append(
        calculate_annual_debt_service(cost, 25, itc=True, interest_rate=0.04) + OPERATION_COSTS)
    debt_services.append(
        calculate_annual_debt_service(cost, 30, itc=True, interest_rate=0.04) + OPERATION_COSTS)

# split into residential and commercial
debt_services_com = debt_services[6:]
debt_services = debt_services[:6]

# plot all possible debt services
plt.figure(figsize=(10, 6))
# plt.plot(solar_capacities, debt_services[0], label='Debt Service no commercial')
# plt.plot(solar_capacities, debt_services[0], label='Debt Service no commercial + (ITC)')
# plt.plot(solar_capacities, debt_services[2], label='Debt Service with commercial')
# plt.plot(solar_capacities, debt_services[3], label='Debt Service with commercial + (ITC)')

# %%
# in order to maintain a DSCR of 1.25, the net operating income must be at least 1.25 times the annual debt service
# calculate the energy rate required to meet the DSCR threshold
# solar_generations_cap = [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21]
solar_generations_cap = [0.13, 0.16, 0.21]

solar_capacities = np.array(solar_capacities)

# a list of numpy arrays to store the maximum possible production
solar_generation_kwh = []

# residential solar generation
for cap in solar_generations_cap:
    solar_generation_kwh.append(solar_capacities * cap * 24 * 365)

# consider case if solar generation needs to sell electricity back to grid at lower rate
# outflow_rates = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
outflow_rate = 0.2
OUTFLOW_DISCOUNT_FACTOR = 2 / 3
temp_arr = []
# if outflow_rate > 0:
# for solar_generations in solar_generation_kwh:
    # temp_arr.append(solar_generations * (1 - outflow_rate + OUTFLOW_DISCOUNT_FACTOR * outflow_rate))

solar_generation_kwh.extend(temp_arr)

net_operating_incomes = DSCR_THRESHOLD * np.array(debt_services)
solar_generation_kwh = np.array(solar_generation_kwh)

energy_rates_res = net_operating_incomes[:, np.newaxis, :] / solar_generation_kwh[np.newaxis, :, :]
# energy_rates_res = energy_rates_res.reshape(len(net_operating_incomes) * len(solar_generation_kwh), 1000)

# %%
DTE_rate = 0.1522

# plot each energy rate
plt.figure(figsize=(10, 6))

plt.plot(solar_capacities, energy_rates_res[1], label='0.162')
plt.plot(solar_capacities, energy_rates_res[7], label='0.162 + ITC')
plt.plot(solar_capacities, DTE_rate * np.ones(1000), color='r', linestyle='--', label='DTE Rate ($0.1522 / kWh)')

# Set fixed y-axis limits
plt.ylim(0.10, 0.225)
plt.yticks(np.linspace(0.10, 0.22, 13))

plt.xlabel('Solar Capacity (kW)')
plt.ylabel('Energy Rate ($/kWh)')
plt.title('Energy Rate vs. Solar Generation Cost (No Commercial Participation)')
plt.legend()
plt.show()

# %%
plt.plot(solar_capacities, energy_rates_res[0][1], label='15 year, 0.0345')
plt.plot(solar_capacities, energy_rates_res[1][1], label='25 year, 0.0345')
plt.plot(solar_capacities, energy_rates_res[2][1], label='30 year, 0.0345')
plt.plot(solar_capacities, energy_rates_res[3][1], label='15 year, 0.04')
plt.plot(solar_capacities, energy_rates_res[4][1], label='25 year, 0.04')
plt.plot(solar_capacities, energy_rates_res[5][1], label='30 year, 0.04')

plt.fill_between(solar_capacities, energy_rates_res[1][0], energy_rates_res[1][2], color='green', alpha=0.3)
plt.plot(solar_capacities, DTE_rate * np.ones(1000), color='r', linestyle='--', label='DTE Rate ($0.1522 / kWh)')

# Set fixed y-axis limits
plt.ylim(0.10, 0.225)
plt.yticks(np.linspace(0.10, 0.22, 13))

plt.xlabel('Solar Capacity (kW)')
plt.ylabel('Energy Rate ($/kWh)')
plt.title('Different Loan Terms and Interest Rates at 0.16 Efficiency')
plt.legend()
plt.show()

# %%
# do the same but factor commercial participation
solar_generation_kwh_com = []

# commercial solar generation
for cap in solar_generations_cap:
    solar_generation_kwh_com.append((solar_capacities + TOTAL_COMMERCIAL * 100) * cap * 24 * 365)

temp_arr = []
# if outflow_rate > 0:
# for solar_generations in solar_generation_kwh_com:
#     temp_arr.append(solar_generations * (1 - outflow_rate + OUTFLOW_DISCOUNT_FACTOR * outflow_rate))

# solar_generation_kwh_com.extend(temp_arr)

solar_generation_kwh_com = np.array(solar_generation_kwh_com)

net_operating_incomes_com = DSCR_THRESHOLD * np.array(debt_services[6:])

energy_rates_com = net_operating_incomes_com[1:2, np.newaxis, :] / solar_generation_kwh_com[np.newaxis, :, :]
energy_rates_com = energy_rates_com.reshape(len(solar_generation_kwh_com), 1000)

# %%
# plot each energy rate
plt.figure(figsize=(10, 6))
plt.plot(solar_capacities, energy_rates_com[0], label='0.132')
plt.plot(solar_capacities, energy_rates_com[1], label='0.162')
plt.plot(solar_capacities, energy_rates_com[2], label='0.212')
plt.fill_between(solar_capacities, energy_rates_com[0], energy_rates_com[2], color='green', alpha=0.3)

# Set fixed y-axis limits
plt.ylim(0.10, 0.225)
plt.yticks(np.linspace(0.10, 0.22, 13))

plt.plot(solar_capacities, DTE_rate * np.ones(1000), color='r', linestyle='--', label='DTE Rate')
plt.xlabel('Solar Capacity (kW)')
plt.ylabel('Energy Rate ($/kWh)')
plt.title('Energy Rate vs. Solar Generation Cost Including Commercial Participation')
plt.legend()
plt.show()
