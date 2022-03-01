library(lmerTest)
library(ggplot2)

rm(list=ls())


taimushum<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20211103-1125-tinyalchemy-immediateusageWithoutLog-Memory-human.csv")
taimusran<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20211103-1125-tinyalchemy-immediateusageWithoutLog-Memory-random.csv")
tpimushum<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20211103-1125-tinypixels-immediateusageWithoutLog-Memory-human.csv")
tpimusran<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20211103-1125-tinypixels-immediateusageWithoutLog-Memory-random.csv")

tphumdf<-data.frame(emp = (c(tpimushum$x1)),
                   prob = c(tpimushum$y))

tprandf<-data.frame(emp = (c(tpimusran$x1)),
                    prob = c(tpimusran$y))
tahumdf<-data.frame(emp = (c(taimushum$x1)),
                    prob = c(taimushum$y))

tarandf<-data.frame(emp = (c(taimusran$x1)),
                    prob = c(taimusran$y))


tphumdf$prob <- as.numeric(as.character(tphumdf$prob))
tprandf$prob <- as.numeric(as.character(tprandf$prob))
tahumdf$prob <- as.numeric(as.character(tahumdf$prob))
tarandf$prob <- as.numeric(as.character(tarandf$prob))

tphumdf$emp_scaled <- scale(as.numeric(as.character(tphumdf$emp)))
tprandf$emp_scaled <- scale(as.numeric(as.character(tprandf$emp)))
tahumdf$emp_scaled <- scale(as.numeric(as.character(tahumdf$emp)))
tarandf$emp_scaled <- scale(as.numeric(as.character(tarandf$emp)))


tpkendalcorhum<- cor.test(tphumdf$emp, tphumdf$prob, method='kendal')
tpkendalcorhum
tpkendalcorran<- cor.test(tprandf$emp, tprandf$prob, method='kendal')
tpkendalcorran
takendalcorhum<- cor.test(tahumdf$emp, tahumdf$prob, method='kendal')
takendalcorhum
takendalcorran<- cor.test(tarandf$emp, tarandf$prob, method='kendal')
takendalcorran

kendall.ci<-function (x=NULL, y=NULL, alpha=0.05, type="t", bootstrap=F, B=1000, example=F) 
{
  #Taken from NSM3: Functions and Datasets to Accompany Hollander, Wolfe, and Chicken - Nonparametric Statistical Methods, Third Edition
  
  # This will produce a 1 - alpha CI for
  # Kendall's tau.  Based on sections 8.3 and 8.4 of:
  #
  #   Nonparametric Statistical Methods, 3e
  #   Hollander, Wolfe & Chicken 
  #
  # bootstrap = F will find the asymptotic CI as in section 8.3.
  # bootstrap = T will find a bootstrap CI as in section 8.4
  # type can be "t" (two-sided), "u" (upper) or "l" (lower).
  # B is the number of bootstrap replicates.
  #
  # Inefficiently programmed by Eric Chicken, October 2012.
  
  # Example 8.1 from HW&C
  if(example)
  {
    x <- c(44.4, 45.9, 41.9, 53.3, 44.7, 44.1, 50.7, 45.2, 60.1)
    y <- c(2.6, 3.1, 2.5, 5, 3.6, 4, 5.2, 2.8, 3.8)
  }
  
  continue <- T
  
  if(is.null(x) | is.null(y)) 
  {	
    cat("\n")
    cat("You must supply an x sample and a y sample!", "\n")
    cat("\n")
    continue <- F
  }
  
  if(continue & (length(x) != length(y))) 
  {	
    cat("\n")
    cat("Samples must be of the same length!", "\n")
    cat("\n")
    continue <- F
  }
  
  if(continue & (length(x) <= 1)) 
  {	
    cat("\n")
    cat("Sample size n must be at least two!", "\n")
    cat("\n")
    continue <- F
  }
  
  if(continue & (type!="t" & type!="l" & type!="u")) 
  {	
    cat("\n")
    cat("Argument \"type\" must be one of \"s\" (symmetric), \"l\" (lower) or \"u\" (upper)!", "\n")
    cat("\n")
    continue <- F
  }
  
  # Q* from (8.17)
  Q <- function(i, j)
  {
    Q.ij <- 0
    ij <- (j[2] - i[2]) * (j[1] - i[1])
    if(ij > 0) Q.ij <- 1
    if(ij < 0) Q.ij <- -1
    Q.ij
  }
  
  # C.i from (8.37)
  C.i <- function(x, y, i)
  {
    C.i <- 0
    for(k in 1:length(x))
      if(k != i) 
        C.i <- C.i + Q(c(x[i], y[i]), c(x[k], y[k]))
      C.i		
  }
  
  if(continue & !bootstrap)
  {
    c.i <- numeric(0)
    n <- length(x)
    for(i in 1:n) c.i <- c(c.i, C.i(x, y, i))
    
    # Get the estimate of tau from the existing function cor.test
    # (8.34)
    # Temporarily disable warnings about p-values and ties
    options("warn" = -1)
    tau.hat <- cor.test(x, y, method="k")$estimate
    options("warn" = 0)
    
    # (8.38)
    sigma.hat.2 <- 2 * (n - 2) * var(c.i) / n / (n-1)
    sigma.hat.2 <- sigma.hat.2 + 1 - (tau.hat)^2
    sigma.hat.2 <- sigma.hat.2 * 2 / n / (n - 1)
    
    if(type=="t") z <- qnorm(alpha / 2, lower.tail = F)
    if(type!="t") z <- qnorm(alpha, lower.tail = F)
    # (8.39), (8.43), (8.45)
    tau.L <- tau.hat - z * sqrt(sigma.hat.2)
    tau.U <- tau.hat + z * sqrt(sigma.hat.2)
    if(type=="l") tau.U <- 1
    if(type=="u") tau.L <- -1
  }
  
  if(continue & bootstrap)
  {
    tau <- numeric(0)
    for(b in 1:B)
    {
      b.sample <- sample(1:length(x), length(x), replace=T)
      # Temporarily disable warnings about p-values and ties
      options("warn" = -1)
      tau.sample <- cor.test(x[b.sample], y[b.sample], method="k")
      options("warn" = 0)
      tau.sample <- tau.sample$estimate
      tau <- c(tau, tau.sample)
    }
    tau.hat <- sort(tau)
    hist(tau.hat)
    if(type=="t") k <- floor((B + 1) * alpha / 2)
    if(type!="t") k <- floor((B + 1) * alpha)
    tau.L <- tau.hat[k]
    tau.U <- tau.hat[(B + 1 - k)]
    if(type=="l") tau.U <- 1
    if(type=="u") tau.L <- -1
    
  }
  
  tau.L <- round(tau.L, 3)
  tau.U <- round(tau.U, 3)
  
  if(type=="t") print.type <- " two-sided CI for tau:"
  if(type=="l") print.type <- " lower bound for tau:"
  if(type=="u") print.type <- " upper bound for tau:"
  
  cat("\n")
  cat(paste("1 - alpha = ", 1 - alpha, print.type, sep=""))
  cat("\n")
  cat(paste(tau.L, ", ", tau.U, sep=""), "\n")
  cat("\n")
  
}


tphumanci <- kendall.ci(x=tphumdf$emp, y=tphumdf$prob, alpha=0.05, type="t", bootstrap=F, B=1000, example=F)
tprandomci <- kendall.ci(x=tprandf$emp, y=tprandf$prob, alpha=0.05, type="t", bootstrap=F, B=1000, example=F) 
tahumanci <- kendall.ci(x=tahumdf$emp, y=tahumdf$prob, alpha=0.05, type="t", bootstrap=F, B=1000, example=F)
tarandomci <- kendall.ci(x=tarandf$emp, y=tarandf$prob, alpha=0.05, type="t", bootstrap=F, B=1000, example=F) 

