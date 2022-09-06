library(lmerTest)
library(ggplot2)

rm(list=ls())


dta<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1425-tinyalchemy-valuedifferences-human-1.csv')
dtp<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1434-tinypixels-valuedifferences-human-1.csv')

dat<-data.frame(trial=scale(c(dta$trial, dtp$trial)),
                id=paste(c(dta$id, dtp$id+1000)), 
                cbu=scale(c(dta$delta_cbu, dtp$delta_cbu)),
                emp=scale(c(dta$delta_emp, dtp$delta_emp)),
                bin=scale(c(dta$delta_bin, dtp$delta_bin)),
                decision=c(dta$decision, dtp$decision),
                game=c(rep('alchemy', nrow(dta)) ,rep('pixel', nrow(dtp))))


mfull1<-glmer(decision~-1+cbu+emp+game+game*emp+game*cbu+trial+trial*emp+trial*cbu+(1|id), family='binomial', data=dat)
ms<-summary(mfull1)
alechmym<-ms$coefficients[1:2,1]
alchemyse<-ms$coefficients[1:2,2]
ms

dat$game<-relevel(dat$game, ref='pixel')

mfull2<-glmer(decision~-1+cbu+emp+game+game*emp+game*cbu+trial+trial*emp+trial*cbu+(1|id), family='binomial', data=dat)
ms<-summary(mfull2)
pixelm<-ms$coefficients[1:2,1]
pixelmse<-ms$coefficients[1:2,2]
dp<-data.frame(mu=c(alechmym, pixelm), ci=1.96*c(alchemyse, pixelmse),
               game=rep(c('Tiny Alchemy', 'Tiny Pixels'), each=2),
               model=rep(c('Uncertainty', 'Empowerment'), 2))

ms

#limits with 95% CIs
limits <- aes(ymax = mu + ci, ymin= mu - ci)

#plot
p <- ggplot(dp, aes(x=model, y=mu)) +
  #bars
  geom_bar(position="dodge", stat="identity", width=0.6)+
  #error bars
  geom_errorbar(limits, position="dodge", width=0.25)+
  #points
  geom_point(size=3)+
  #color
  #scale_fill_manual(values = c(cbPalette))+
  #theme
  theme_minimal() +
  #limits
  #scale_y_continuous(limits = c(0,100), expand = c(0, 0)) +
  #two facets
  facet_wrap(~game, nrow=2)+
  #labs
  xlab("Model")+
  ylab(expression(beta))+
  #title
  ggtitle("")+
  #adjust text size
  theme(text = element_text(size=21,  family="sans"))+
  #no legend
  theme(legend.position = "none")

#png('modelcomparison.png', width=350, height=450)
p
dp

tadf<-data.frame(trial=scale(dta$trial),
                 id=paste(dta$id), 
                 cbu=scale(dta$delta_cbu),
                 emp=scale(dta$delta_emp),
                 bin=scale(dta$delta_bin),
                 cbv=scale(dta$delta_cbv),
                 truebin=scale(dta$delta_truebin),
                 trueemp=scale(dta$delta_trueemp),
                 decision=dta$decision)

tpdf<-data.frame(trial=scale(dtp$trial),
                 id=paste(dtp$id), 
                 cbu=scale(dtp$delta_cbu),
                 emp=scale(dtp$delta_emp),
                 bin=scale(dtp$delta_bin),
                 cbv=scale(dtp$delta_cbv),
                 truebin=scale(dtp$delta_truebin),
                 trueemp=scale(dtp$delta_trueemp),
                 decision=dtp$decision)

#comparison emp & unc in TA
emp_df <- subset(tadf, select=c("emp","decision", "id", "trial"))
emp_df$empmodel <- 1
names(emp_df)[names(emp_df) == "emp"] <-"modelestimate"

cbu_df <- subset(tadf, select=c("cbu","decision", "id", "trial"))
cbu_df$empmodel <- 0
names(cbu_df)[names(cbu_df) == "cbu"] <-"modelestimate"

concatenated_df<-rbind(emp_df,cbu_df)
concatenated_df_fullregression<-glmer(decision~-1+modelestimate+modelestimate*empmodel+trial+trial*modelestimate+(1|id), family='binomial', data=concatenated_df, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(concatenated_df_fullregression)

#comparison emp & unc in TP
emp_df <- subset(tpdf, select=c("emp","decision", "id", "trial"))
emp_df$empmodel <- 1
names(emp_df)[names(emp_df) == "emp"] <-"modelestimate"

cbu_df <- subset(tpdf, select=c("cbu","decision", "id", "trial"))
cbu_df$empmodel <- 0
names(cbu_df)[names(cbu_df) == "cbu"] <-"modelestimate"

concatenated_df<-rbind(emp_df,cbu_df)
concatenated_df_fullregression<-glmer(decision~-1+modelestimate+modelestimate*empmodel+trial+trial*modelestimate+(1|id), family='binomial', data=concatenated_df, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(concatenated_df_fullregression)
