##simplecovid##
**Aggregation and plotting of covid case, death, test, and hospitalization data for U.S. and States**
In this project I did research aggregating and analyzing mortality data for the U.S. aggregate as well as individual states. Sources were CDC, U.S. Census Bureau, both federal and state Departments of Public Health, and other governmental agencies and NGO's. For COVID-19 data my primary sources were the nytimes and johns hopkins github repos. I've also pulled observed deaths from Georgia DPH, and CDC. This is an evolving work-in-progress, I wanted to both build my python skills with matplotlib and plotly to report on covid cases and deaths, then I also got into the idea of analyzing historic mortality versus what we've observed this year and plotting variance which is likely attributable to covid-19.
Identifying increased aggregate mortality is likely a better measure of the true impact of this virus for three reasons:

1. there are an unknown number of deaths that occured at home or other non-hospital locations and went unrecorded or were recorded without the U07.1 classifier for covid-19
2. quite a few deaths have likely been due to covid-19 but the ME either didn't test the patient post-mortem or didn't record it correctly (for example, there was another illness and it was listed as the underlying cause)
3. there are deaths from other causes during lockdown that were due to the unavailability of healthcare or medicines (the 'acute' period would have been from mid-march to mid-may). This increase in mortality could be called the systemic disruption of everyday life due to pandemic.
I've had to refactor my code as my focus has evolved on this project, this is still a rough w-i-p but if it helps anyone, great! I apologize for the need for refactoring.
