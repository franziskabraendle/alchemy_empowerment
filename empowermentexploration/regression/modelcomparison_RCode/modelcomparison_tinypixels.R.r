library(lmerTest)
library(ggplot2)

rm(list=ls())
tp<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1434-tinypixels-valuedifferences-human-1.csv')

tpdf<-data.frame(trial=scale(tp$trial),
                  id=paste(tp$id), 
                  cbu=scale(tp$delta_cbu),
                  emp=scale(tp$delta_emp),
                  bin=scale(tp$delta_bin),
                  cbv=scale(tp$delta_cbv),
                  truebin=scale(tp$delta_truebin),
                  trueemp=scale(tp$delta_trueemp),
                  decision=tp$decision)

# 
## BOTTOM UP ANALYSIS
# get model with single models as fixed effect
me <- glmer(decision ~ -1 + emp + trial + trial*emp + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(me)

mv <- glmer(decision ~ -1 + cbv + trial + trial*cbv + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mv)

mb <- glmer(decision ~ -1 + bin + trial + trial*bin + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mb)

mu <- glmer(decision ~ -1 + cbu + trial + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mu)

# get model with empowerment and binary as fixed effect
meb <- glmer(decision ~ -1 + emp + bin + trial + trial*emp + trial*bin + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meb)

# get model with empowerment and CBU as fixed effect
meu <- glmer(decision ~ -1 + emp + cbu + trial + trial*emp + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meu)

# get model with binary and CBU as fixed effect
mub <- glmer(decision ~ -1 + bin + cbu + trial + trial*bin + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mub)

# get model with empowerment and binary and CBU as fixed effect
meub <- glmer(decision ~ -1 + emp + bin + cbu + trial + trial*emp + trial*bin + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meub)

trueemp_regression <-glmer(decision ~ -1 + trueemp + trial + trial*trueemp + (1|id), data=tpdf, family="binomial")
summary(trueemp_regression)

trueemp_regression_wot <-glmer(decision ~ -1 + trueemp + (1|id), data=tpdf, family="binomial")
summary(trueemp_regression_wot)

truebin_regression <-glmer(decision ~ -1 + truebin + trial + trial*truebin + (1|id), data=tpdf, family="binomial")
summary(truebin_regression)

truecomb_regression <-glmer(decision ~ -1 + truebin + trueemp + trial + trial*truebin + trial*trueemp + (1|id), data=tpdf, family="binomial")
summary(truecomb_regression)

truecomb_regression_wot <-glmer(decision ~ -1 + trueemp + truebin + (1|id), data=tpdf, family="binomial")
summary(truecomb_regression_wot)

