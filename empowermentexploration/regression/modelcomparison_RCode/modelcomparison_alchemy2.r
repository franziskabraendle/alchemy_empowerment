library(lmerTest)
library(ggplot2)

rm(list=ls())

la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20220824-1210-alchemy2-valuedifferences-human-1.csv") #not matched, like original gametree, with rec and inventory (used gametree from 5.8.21, all files self created - clean)
#la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20220825-1119-alchemy2-valuedifferences-human-1.csv") #matched, like original gametree, with rec and inventory (used gametree from 5.8.21, all files self created - clean)
#la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20220826-1046-alchemy2-valuedifferences-human-1.csv") #not matched, new emp model, with rec and inventory (used gametree from 18.5.22, - clean)
#la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20221108-1655-alchemy2-valuedifferences-human-0.csv") #not matched, like original gametree, with rec and inventory (used gametree from 5.8.21, all files self created - clean), no memory


la2df<-data.frame(trial=scale(la2$trial),
                  id=paste(la2$id), 
                  inventory=scale(la2$inventory), 
                  cbu=scale(la2$delta_cbu),
                  rec=-1*scale(la2$delta_rec),
                  emp=scale(la2$delta_emp),
                  bin=scale(la2$delta_bin),
                  cbv=scale(la2$delta_cbv),
                  truebin=scale(la2$delta_truebin),
                  trueemp=scale(la2$delta_trueemp),
                  decision=la2$decision)

## BOTTOM UP ANALYSIS
# get model with single models as fixed effect
me <- glmer(decision ~ -1 + emp + trial + trial*emp + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(me)

mv <- glmer(decision ~ -1 + cbv + trial + trial*cbv + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mv)

mb <- glmer(decision ~ -1 + bin + trial + trial*bin + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mb)

mu <- glmer(decision ~ -1 + cbu + trial + trial*cbu + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mu)

mr <- glmer(decision ~ -1 + rec + trial + trial*rec + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mr)

# get model with empowerment and binary as fixed effect
meb <- glmer(decision ~ -1 + emp + bin + trial + trial*emp + trial*bin + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meb)

# get model with empowerment and CBU as fixed effect
meu <- glmer(decision ~ -1 + emp + cbu + trial + trial*emp + trial*cbu + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meu)

# get model with binary and CBU as fixed effect
mub <- glmer(decision ~ -1 + bin + cbu + trial + trial*bin + trial*cbu + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mub)

mer <- glmer(decision ~ -1 + emp + rec + trial + trial*emp + trial*rec + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mer)

mbr <- glmer(decision ~ -1 + bin + rec + trial + trial*bin + trial*rec + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mbr)

mur <- glmer(decision ~ -1 + cbu + rec + trial + trial*cbu + trial*rec + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "Nelder_Mead")) #NOTWORKING
summary(mur)

meub <- glmer(decision ~ -1 + emp + bin + cbu + trial + trial*emp + trial*bin + trial*cbu + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meub)

meur <- glmer(decision ~ -1 + emp + cbu + rec + trial + trial*emp + trial*cbu + trial*rec + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meur)

mebr <- glmer(decision ~ -1 + emp + bin + rec + trial + trial*emp + trial*bin + trial*rec + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mebr)

mbur <- glmer(decision ~ -1 + rec + bin + cbu + trial + trial*rec + trial*bin + trial*cbu + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "Nelder_Mead")) #NOTWORKING
summary(mbur)

meuri <- glmer(decision ~ -1 + emp + cbu + trial + rec + inventory + trial*emp + trial*cbu + trial*rec + trial*inventory + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meuri)

meubri <- glmer(decision ~ -1 + emp + bin + cbu + rec + inventory + trial + trial*emp + trial*bin + trial*cbu + trial*rec + trial*inventory + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meubri)

#check values without including trial

meubriot <- glmer(decision ~ -1 + emp + bin + cbu + rec + inventory + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meubriot)

mburot <- glmer(decision ~ -1 + rec + bin + cbu + (1 | id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mburot)

#check values based on true gametree

trueemp_regression <-glmer(decision ~ -1 + trueemp + trial + trial*trueemp + (1|id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(trueemp_regression)

trueemp_regression_wot <-glmer(decision ~ -1 + trueemp + (1|id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(trueemp_regression_wot)

truebin_regression <-glmer(decision ~ -1 + truebin + trial + trial*truebin + (1|id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(truebin_regression)

truecomb_regression <-glmer(decision ~ -1 + truebin + trueemp + trial + trial*truebin + trial*trueemp + (1|id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(truecomb_regression)

truecomb_regression_wot <-glmer(decision ~ -1 + trueemp + truebin + (1|id), data=la2df, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(truecomb_regression_wot)

# check difference between emp and cbu

emp_df <- subset(la2df, select=c("emp","decision", "id", "trial"))
emp_df$empmodel <- 1
names(emp_df)[names(emp_df) == "emp"] <-"modelestimate"

cbu_df <- subset(la2df, select=c("cbu","decision", "id", "trial"))
cbu_df$empmodel <- 0
names(cbu_df)[names(cbu_df) == "cbu"] <-"modelestimate"

concatenated_df<-rbind(emp_df,cbu_df)
concatenated_df_fullregression<-glmer(decision~-1+modelestimate+modelestimate*empmodel+trial+trial*modelestimate+(1|id), family='binomial', data=concatenated_df, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(concatenated_df_fullregression)
