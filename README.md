# Open BSEC for BME680

### Abstract
BME680 is a gas sensor produced by Bosch. It claims that it can give IAQ(indoor air quilty) and CO2 equivalents, as well as many other gas indexes, include bVOC(breath VOC) and s-IAQ(static IAQ). However, it can only give a gas resistance in Ohm. Customers need a closed-source user-unfriendly software BSEC(Bosch Software Environmental Cluster) to get IAQ and CO2 from gas resistance. In this repository the mechanism of BME680 and the behavior of BSEC are studied thoroughly. Then an open-source substitution for BSEC is provided.

### How BME680 works
BME680 uses a MOS resistor to detect reducing gases -- such as Ethanol, Formaldehyde and Carbon monoxide(unfortunately, CO2 is not included) -- and then estimate IAQ, CO2 equivalents and other indexes. The exact type of MOS BME680 used is believed to be TiO2. In clean air, donor electrons in tin dioxide are attracted toward oxygen which is adsorbed on the surface of the sensing material, preventing electric current flow. In the presence of reducing gases, the surface density of adsorbed oxygen decreases as it reacts with the reducing gases. Electrons are then released into the tin dioxide, allowing current to flow freely through the sensor. So lower resistance means worse IAQ. The MOS needs to be heated so that oxygen can be adsorbed on the surface. The theoretical formula of sensor resistances R reads

R/R_0 = N_d/e_S

e_S = N_d exp{-(1/6)(a/L_D)^2 - p}

Here e_S is the surface electron concentration and L_D is the Debye length. R0 is the sensor resistances when there is no reducing gases. a	is Particle radius. When sensor is made, N_d, a, L_D and R_0 are fixed, while p is dependent on the actual gaseous conditions. So the equivalent reducing gas pressure reads

\delta p = C (A + B/T - ln(R))

where B and C are constants of the sensor, and A needs to be calibrated based on the history after power on. Readers will soon find that how A is calibrated by BSEC is the main issue. 

As discussed above, BME680 is enough for demand controlled ventilation(DCV) while it cannot give exact value of any of IAQ or CO2 equivalents.

### bVOC and s-IAQ as a function of CO2 equivalents

### How CO2 equivalents is calculated

### Discussion
