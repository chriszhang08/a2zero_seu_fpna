# README: Solar Energy Debt Modeling and Energy Rate Analysis

## Overview

This repository contains a Python model that analyzes the financial feasibility of the Sustainable Energy Utility
that Ann Arbor is proposing. The model calculates the debt service costs of solar installations, estimates the energy 
rates required to meet financial thresholds, and compares them with current utility rates (such as DTE Energy).

The model primarily focuses on evaluating the impact of different solar capacities, financing terms, and tax incentives 
on the energy rate required for solar projects to be viable. The key metrics include debt service coverage ratio (DSCR), 
energy generation capacity, and the federal solar Investment Tax Credit (ITC).

## Key Features

1. **Debt Service Calculation**: 
   - The model calculates the **annual debt service** for solar projects based on loan terms, interest rates, and the inclusion of the federal ITC (Investment Tax Credit), which reduces the principal by 30%.
   - The formula used for debt service is based on fixed-rate loan amortization, which ensures accuracy in calculating the annual loan payments.

2. **Startup and Commercial Costs**:
   - The model considers startup costs of $400,000 as well as **commercial solar installation costs** for apartments and hotels.
   - It calculates additional costs for **commercial battery installations**, assuming a 60 kW battery system with a 4-hour discharge cycle at $400/kWh.

3. **Energy Rate Determination**:
   - The model computes the **required energy rates** (in $/kWh) to meet a minimum DSCR of 1.25, which ensures the 
   project generates sufficient revenue to cover debt service.
   - It considers multiple solar generation efficiencies (capacity factors) and compares energy rates for different loan 
   terms (15, 25, 30 years) and interest rates (3.45%, 4%).
   - The calculation is simply the required revenue divided by the total energy generated, 
   factoring in the ITC and debt service.

4. **Incorporation of Commercial Solar**:
   - The model factors in commercial participation (hotels and apartments) and how their participation would affect the energy rates. This is done by increasing the solar capacity and recalculating the total energy generated and the corresponding debt service.

5. **Impact of Outflow Rates**:
   - The model explores scenarios where solar projects sell excess electricity back to the grid at discounted rates, known as **outflow rates**. This affects the net operating income and the required energy rate to cover costs.

6. **Comparison with Utility Rates**:
   - The energy rates calculated by the model are compared to **DTE Energy’s current residential rate of $0.1522/kWh**, allowing a side-by-side comparison of the solar project’s competitiveness.

## Outputs

TODO insert substack link


### Plots Generated
- **Energy Rate vs. Solar Generation Cost (No Commercial Participation)**:
[![Energy Rate vs. Solar Generation Cost (No Commercial Participation)](/imgs/capfactor.png)]
   - A plot that shows the energy rates required for solar projects without commercial participation. 
  It compares different loan terms and interest rates, indicating whether the solar energy rates would be competitive with DTE Energy's current rate.

- **Different Loan Terms and Interest Rates at 0.16 Efficiency**:
   - A plot showing how various loan terms (15, 25, 30 years) and interest rates (3.45%, 4%) affect the required energy rate at a solar capacity factor of 0.16.

- **Energy Rate vs. Solar Generation Cost Including Commercial Participation**:
   - A plot that illustrates the effect of commercial participation (hotels and apartments) on the energy rates. The required rates are compared to DTE's rate, and the impact of different solar generation capacities is highlighted.

### Python Model

The Python model relies on the following libraries:
- **NumPy**: For numerical computations and array manipulations.
- **SciPy**: For statistical calculations and the debt service formula.
- **Matplotlib**: For generating plots to visualize energy rate comparisons.

## Key Article Insights

The accompanying article outlines the financial and operational considerations of implementing solar installations in Ann Arbor. Key points include:
- **Federal Solar Incentives**: The 30% federal Investment Tax Credit (ITC) is a critical incentive for solar projects, reducing the initial cost of solar installations.
- **Michigan Solar Capacity Factor**: Solar generation in Michigan varies between 13% and 21%, with higher outputs in the summer and lower in the winter.
- **Loan Terms and Debt Service**: Financing terms (loan duration and interest rates) are pivotal in determining the feasibility of solar projects. The model assesses different loan options and calculates the resulting debt service payments.
- **Commercial Participation**: Involving hotels and apartment buildings in the solar project increases the overall capacity, potentially lowering the required energy rate through economies of scale.
- **Net Metering and Outflow Rates**: The model accounts for scenarios where excess electricity is sold back to the grid at discounted rates, which affects the project's revenue and the required energy rate to maintain profitability.

## How to Run the Model

1. Install the required Python libraries:
   ```bash
   pip install numpy scipy matplotlib
   ```

2. Run the Python script to generate plots and see the results.

## Conclusion

This model provides a comprehensive financial analysis of solar energy installations, focusing on debt servicing, energy generation, and profitability. It helps determine the solar capacity and energy rates required for multifamily and commercial properties to adopt solar in a financially sustainable way.