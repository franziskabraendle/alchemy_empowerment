rm(list=ls())

#packages
packages <- c('lmerTest','plyr', 'jsonlite', 'performance')
lapply(packages, library, character.only = TRUE)

#json
mj<-fromJSON('validation_behavior.json')

#empowerment
empowerment<-read.csv("..\\..\\..\\empowermentexploration\\additionalexperiments\\validation_datageneration\\element_empowerment.csv")

#initialize data frame
d<-data.frame(id=numeric(), element=numeric(), pred=numeric(), emp=numeric(), rating=numeric())
for (i in 1:length(mj)){
  #get it
  m<-mj[[i]]
  #empowerment rating
  emp<-as.numeric(m$empowermentanswers)
  #which one
  rand_element<-m$randomempelement
  #predicted emp 
  predicted_emp<-empowerment$emp_value_predicted[empowerment$element_string %in% rand_element]
  #true emp
  true_emp<-empowerment$emp_value_true[empowerment$element_string %in% rand_element]
  #id
  id<-rep(i, length(true))
  #bind
  d<-rbind(d, data.frame(id=i, element=rand_element, pred=predicted_emp, emp=true_emp, rating=emp))
}

#regress onto rating, we log because of non-normal dist
m1<-lmer(rating~scale(log(pred+0.1))+scale(log(emp+0.1))+(1|id), data=d)
#summary
summary(m1)
#r2
r2(m1)

#taken alone
m2<-lmer(rating~scale(log(emp+0.1))+(1|id), data=d)
#summary
summary(m2)
#r2
r2(m2)

#prediction frame
prediction<-read.csv("..\\..\\..\\empowermentexploration\\additionalexperiments\\validation_datageneration\\prediction_selection.csv")
#initialize
d<-data.frame(id=numeric(), pred=numeric(), outcome=numeric(), rating=numeric())
#loop through
for (i in 1:length(mj)){
  #select
  m<-mj[[i]]
  #initialize
  probpred<-outcome<-numeric()
  #go through all choices
  for (k in 1:nrow(m$currentcombinationstring)){
    #which one did they see?
    mark<-which(paste(prediction$first_string) %in% m$currentcombinationstring[k,1] & paste(prediction$second_string) %in% m$currentcombinationstring[k,2])
    #what was the predicted prob of the comb being successful
    probpred<-c(probpred, prediction$predSuccess[mark])
    #what would actually come out
    outcome<-c(outcome, paste(prediction$result_string[mark]))
  }
  #what did they say?
  probs<-as.numeric(m$linkanswers)
  #bind
  d<-rbind(d, data.frame(id=i, pred=probpred, outcome=outcome, rating=probs))
}

#see how prediction matches rating
m3<-lmer(rating~scale(pred)+(1|id), data=d)
#summarize
summary(m3)
#r2
r2(m3)

#just for element combs that weren't successes according to game tree
m4<-lmer(rating~scale(pred)+(1|id), data=subset(d, outcome=='None'))
#summarize
summary(m4)
#r2
r2(m4)


#initialize frame for probs of which element they chose
d<-data.frame(prob=numeric(), probnot=numeric(), outcome=numeric(), id=numeric())
#loop through
for (i in 1:length(mj)){
  #select
  m<-mj[[i]]
  #initialize
  prob<-probnot<-outcome<-numeric()
  for (k in 1:length(m$randomcombinations)){
    #which one (note +1 conversion because js to R)
    current<-prediction[m$randomcombinations[k]+1,]
    #get answers
    mark<-which(current[,17:20]==m$elementanswers[k])
    #the ones they didn't choose
    notmark<-(1:4)[-mark]
    #sample one of the non-chosen
    notmark<-sample(notmark, 1)
    #standardize prob of chosen
    prob<-c(prob, as.numeric(current[,9:12][mark]/sum(current[,9:12])))
    #standardize prob of not chosen
    probnot<-c(probnot, as.numeric(current[,9:12][notmark]/sum(current[,9:12])))
    #what came actually out
    outcome<-c(outcome, paste(current$result_string))
  }
  #bind to data frame
  d<-rbind(d, data.frame(prob, probnot, outcome, id=i))
}

#get means for both probs
dd<-ddply(d, ~id, summarise, m1=mean(prob), m2=mean(probnot))
#compare via t-test
t.test(dd$m1, dd$m2, var.equal = TRUE)
#Cohens d
cohensD(dd$m1, dd$m2)
#get them for combs that wouldn't return an element
dd<-ddply(subset(d, outcome=='None'), ~id, summarise, m1=mean(prob), m2=mean(probnot))
#get t-test
t.test(dd$m1, dd$m2)
#cohens d
cohensD(dd$m1, dd$m2)

#sample random position 
d$random<-runif(nrow(d))
#assign left or right
d$diff<-ifelse(d$random>0.5, d$prob-d$probnot, d$probnot-d$prob)
#assign fictitious choice
d$choice<-ifelse(d$random>0.5, 1, 0)
#regress differences
m4<-glmer(choice~-1+scale(diff)+(-1+scale(diff)|id), family='binomial', data=d)
#check summary
summary(m4)
#r2
r2(m4)
#do with interaction of outcome 'none'
d$outnone<-ifelse(d$outcome=='None', 1, 0)
#compute
m4<-glmer(choice~-1+scale(diff)*outnone+(1|id), family='binomial', data=d)
#summarize
summary(m4)


