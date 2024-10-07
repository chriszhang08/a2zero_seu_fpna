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
CAPACITY_FACTOR = 0.212

# assume 3.3% interest rate on debt
DEBT_INTEREST_RATE = 0.0345
DSCR_THRESHOLD = 1.25

# potential sensitivity Call Provisions: Callable Bonds
# other initial costs
STARTUP_COSTS = 400000

# %%
# Given values for debt service calculation
interest_rate = 0.04  # 4% annual interest rate
loan_term_years = 25  # 25-year loan


# Formula to calculate annual debt service for a fixed-rate loan
def calculate_annual_debt_service(principal, interest_rate, loan_term_years, itc=False):
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
NUM_SCHOOLS = 20  # ASSUMPTION only 20 schools in Ann Arbor will participate in the program

TOTAL_COMMERCIAL = NUM_APTS + NUM_HOTELS + NUM_SCHOOLS
# each commercial building will have a 100 kW solar system
COMMERCIAL_SOLAR_PER_KW = 2212
COMMERCIAL_COSTS = TOTAL_COMMERCIAL * COMMERCIAL_SOLAR_PER_KW * 100

# %%
# plot annual debt service of solar generation as a function of solar capacity
solar_capacities = np.linspace(10000, 100000, 1000)
solar_generation_costs = SOLAR_PER_KW * solar_capacities
# add startup costs to the solar generation costs
solar_generation_costs += STARTUP_COSTS
# apply the debt service formula to each solar generation cost
debt_services = calculate_annual_debt_service(solar_generation_costs, interest_rate, loan_term_years, itc=True)

# add variable costs to the debt service
debt_services += 500100

plt.figure(figsize=(10, 6))
plt.plot(solar_capacities, debt_services, label='Annual Debt Service')
plt.xlabel('Solar Capacity (kW)')
plt.ylabel('Cost ($)')
plt.title('Annual Debt Service vs. Solar Generation Cost')
plt.legend()
plt.show()

# %%
# in order to maintain a DSCR of 1.25, the net operating income must be at least 1.25 times the annual debt service
# calculate the energy rate required to meet the DSCR threshold
net_operating_incomes = DSCR_THRESHOLD * debt_services
solar_generations = solar_capacities * CAPACITY_FACTOR * 24 * 365
opt_rates = net_operating_incomes / solar_generations

plt.figure(figsize=(10, 6))
plt.plot(solar_capacities, opt_rates, label='Energy Rate')
plt.xlabel('Solar Capacity (kW)')
plt.ylabel('Energy Rate ($/kWh)')
plt.title('Energy Rate vs. Solar Generation Cost')
plt.legend()
plt.show()

# %%
# what if capacity factor drops to 0.152?
NEW_CAPACITY_FACTOR = 0.152
net_operating_incomes = DSCR_THRESHOLD * debt_services
solar_generations = solar_capacities * NEW_CAPACITY_FACTOR * 24 * 365
bad_rates = net_operating_incomes / solar_generations

DTE_rate = 0.1522

# plot on same graph
plt.figure(figsize=(10, 6))
plt.plot(solar_capacities, opt_rates, label='Energy Rate (0.212)')
plt.plot(solar_capacities, bad_rates, label='Energy Rate (0.152)')
plt.axhline(y=DTE_rate, color='r', linestyle='--', label='DTE Rate')
plt.xlabel('Solar Capacity (kW)')
plt.ylabel('Energy Rate ($/kWh)')
plt.title('Energy Rate vs. Solar Generation Cost')
plt.legend()
plt.show()
