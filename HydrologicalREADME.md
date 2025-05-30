data(Çoruh_basin)
InputsModel <- CreateInputsModel(FUN_MOD = RunModel_GR4J, DatesR = Çoruh_basin$DatesR,
                                 Precip = Çoruh_basin$P, PotEvap = Çoruh_basin$E)
Ind_Run <- seq(which(format(Çoruh_basin$DatesR, format = "%Y-%m-%d") == "1985-01-01"),
               which(format(Çoruh_basin$DatesR, format = "%Y-%m-%d") == "2015-12-31"))
RunOptions <- CreateRunOptions(FUN_MOD = RunModel_GR4J,
                               InputsModel = InputsModel, IndPeriod_Run = Ind_Run)
Param <- c(X1 = 259.7, X2 = 3.554, X3 = 18.18, X4 = 18.6)
OutputsModel <- RunModel(InputsModel = InputsModel,
                        RunOptions = RunOptions, Param = Param,
                        FUN_MOD = RunModel_GR4J)
plot(OutputsModel, Qobs = Çoruh_basin$QobsQmm[Ind_Run])


R GR4J çalıştırma kodları
library(airGR)

## loading catchment data
data(L0123001)

## preparation of the InputsModel object
InputsModel <- CreateInputsModel(FUN_MOD = RunModel_GR4J, DatesR = BasinObs$DatesR,
                                 Precip = BasinObs$P, PotEvap = BasinObs$E)

## run period selection
Ind_Run <- seq(which(format(BasinObs$DatesR, format = "%Y-%m-%d")=="1990-01-01"),
               which(format(BasinObs$DatesR, format = "%Y-%m-%d")=="1999-12-31"))

## preparation of the RunOptions object
RunOptions <- CreateRunOptions(FUN_MOD = RunModel_GR4J,
                               InputsModel = InputsModel, IndPeriod_Run = Ind_Run)

## simulation
Param <- c(X1 = 257.238, X2 = 1.012, X3 = 88.235, X4 = 2.208)
OutputsModel <- RunModel_GR4J(InputsModel = InputsModel,
                              RunOptions = RunOptions, Param = Param)

## results preview
plot(OutputsModel, Qobs = BasinObs$Qmm[Ind_Run])

## efficiency criterion: Nash-Sutcliffe Efficiency
InputsCrit  <- CreateInputsCrit(FUN_CRIT = ErrorCrit_NSE, InputsModel = InputsModel,
                                RunOptions = RunOptions, Obs = BasinObs$Qmm[Ind_Run])
OutputsCrit <- ErrorCrit_NSE(InputsCrit = InputsCrit, OutputsModel = OutputsModel)

EŞİK DEĞERLER

library(tidyverse)
uludagStations %>%
  group_by(Year) %>%
  which.max()
summarise(RainMax=max(ULUDAG_Boun_Mgm)) %>%
  ggplot(aes(x=year,y=max)) + geom_line + geom_point
filter(RainPOT=ULUDAG_Boun_Mgm>100)
ggplot(aes(x=yea, y=ULUDAG_Boun_Mgm))+ geom_line + geom_point
ggplot(aes(x=Time, y=ULUDAG_Boun_Mgm))+ geom_line + geom_point

Ekleme
library(tidyverse)
uludagStations %>%
  group_by(Year) %>%
  which.max()
summarise(RainMax=max(ULUDAG_Boun_Mgm)) %>%
  ggplot(aes(x=year,y=max)) + geom_line + geom_point
filter(RainPOT=ULUDAG_Boun_Mgm>0)
ggplot(aes(x=year, y=ULUDAG_Boun_Mgm))+ geom_line + geom_point
ggplot(aes(x=Time, y=ULUDAG_Boun_Mgm))+ geom_line + geom_point
