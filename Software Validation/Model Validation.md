# Hot Gas Model Validation
 PyRegen employs a Bartz type correlation with radiative heat transfer for the modelling of hot gases around the chamber walls.
In the paper linked below you can find graphs of the convective heat transfer coefficient (hc) detailed for multiple cases, varying chamber pressure (Pc) and mixture ratio (MR), and comparisons with CFD results.

 "Hot Gas Model Results" - Experimental results by [B. Betti , D. Liuzzi , F. Nasuti and M. Onofri, 2021], Original Title : " Development of Heat Transfer Correlations
for LOX/CH4 Thrust Chambers"


# Full Model Validation
 The program can be verified in its entirety with results from experiments including different channel sizes, for Hydrolox and Methalox, found in the paper linked below. 

 "Full Model Validation" - Experimental results by [Jan Haemisch, Dmitry Suslov, Michael Oschwald, 2021], available [here](https://www.jstage.jst.go.jp/article/tastj/19/1/19_19.96/_article)

# Important
 <mark>Note that the engine sizes and mass flux have to be calculated by the user according to the chamber pressures given!
 Errors in coolant mass flow or engine size can produce erratic/wrong results, and are a source of significant errors in the calculation!<\mark>
