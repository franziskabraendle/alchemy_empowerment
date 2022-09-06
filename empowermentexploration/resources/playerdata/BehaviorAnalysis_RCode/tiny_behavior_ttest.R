
library(ggplot2)
library(tidyr)
library(rjson)
library(BayesFactor)
library(lsr)

rm(list=ls())

#test if number of trials and size of inventory is significantly different between tinyalchemy and tinypixels

tinyalchemy<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\tinyalchemyHumanDataMemory.csv")
tinypixels<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\tinypixelsHumanDataMemory.csv")

#Code adapted from Charley Wu
#p-values: 3 decimal places of precision; <.001 if the case
pformat <- function(val) { 
  if(val <.001){
    out <- '<.001'
  }else{
    out<-paste0('=',sub("^(-?)0.", "\\1.", sprintf("%.3f", val)))
  }
  return(out)
}

#Cohen's D to a single decimal
dFormat <- function(val) { 
  if (val>=.1){
    paste0('=',sprintf("%.1f", val))
  }else if (val>=.01){
    paste0('=',sprintf("%.2f", val))
  }
  else{
    paste0('=',sprintf("%.2f", val))
  }
}

#Bayes Factor: upper ceiling of 100 as >100, if greater than 1 then display as int, if less than zero show 2 decimal places
bfformat <- function(val, maxValue = 100){
  if (is.na(val)){
    out<- "=NA"
  }else if (val>maxValue){ #If larger than max value, just go with BF>maxValue
    out <- paste0('>',maxValue)
  }else if(val>10){ #if larger than 10 then don't add any decimals
    out<-paste0('=',sprintf("%.0f", val))
  }else if(val>1 & val<10){ #if between 1 and 10 add decimals
    out<-paste0('=',sprintf("%.1f", val))
  }else{ #less than 1, add 2 decimals
    out<-paste0('=',sub("^(-?)0.", "\\1.", sprintf("%.2f", val)))
  }
  return(out)
}

ttestPretty <-function(x,y=NULL,mu=0, var.equal=T, paired=F, maxBF = 100){
  if (!is.null(y)){ #two sample
    freq <- t.test(x,y, var.equal=var.equal, paired = paired)
    d <- cohensD(x = x, y = y)
  }else{ #single sample
    freq <- t.test(x,mu = mu, var.equal=var.equal)
    d <- cohensD(x = x,mu = mu)
  }
  dof <- freq$parameter
  t <- sprintf("%.1f",freq$statistic) 
  p <- pformat(freq$p.value)
  if (!is.null(y)){ #single sample
    BF <-bfformat(extractBF(ttestBF(x,y, paired=paired))$bf, maxValue = maxBF)
  }else{#two sample
    BF <-bfformat(extractBF(ttestBF(x,mu = mu, paired=paired))$bf, maxValue = maxBF)
  }
  return(paste0('$t(',dof,')=',t,'$, $p',p, '$, $d',dFormat(d), '$, $BF',BF,'$'))
}

ta_inventory <- tapply(tinyalchemy$inventory, tinyalchemy$id, max)
tp_inventory <- tapply(tinypixels$inventory, tinypixels$id, max)

df_inventory_ta <- data.frame(ta_inventory)
df_inventory_tp <- data.frame(tp_inventory)

ta_trials <- tapply(tinyalchemy$trial, tinyalchemy$id, max)
tp_trials <- tapply(tinypixels$trial, tinypixels$id, max)

df_trials_ta <- data.frame(ta_trials)
df_trials_tp <- data.frame(tp_trials)

ttestPretty(x = df_inventory_ta$ta_inventory, y = df_inventory_tp$tp_inventory)
ttestPretty(x = df_trials_ta$ta_trials, y = df_trials_tp$tp_trials)
mean(df_trials_ta$ta_trials)
mean(df_trials_tp$tp_trials)
mean(df_inventory_ta$ta_inventory)
mean(df_inventory_tp$tp_inventory)
