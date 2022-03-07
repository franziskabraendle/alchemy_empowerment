library(stringr)
library(png)
setwd("proppics/")

names<-c('utton', 'hep', 'zish', 'tweek', 'trand', 'phlome', 'plunt', 'polb', 
               'flup', 'fluup', 'wous',  'nonc', 'zaen', 'smul', 'coft', 'befo', 'dupp', 
               'vaff', 'temz', 'tasp', 'fauf', 'zomo', 'timb', 'mugo', 'strump', 'mlem', 
               'spri', 'plakt', 'heph', 'shak', 'teme', 'xipon', 'sobit', 'dalit', 'wapor', 
               'retra', 'fdod', 'felu', 'hupp', 'tilf', 'gnoin', 'dermlo', 'fipt', 'glope', 
               'shmost', 'speld', 'myp', 'feuf', 'norg', 'mude', 'stype', 'zuph', 'urst', 
               'shlup', 'gnarb', 'doyng', 'plaughn', 'knorbs', 'rueln', 'moirn', 'bieb',
               'zudd', 'nend', 'lohl', 'kursh', 'thiph')

files <- (Sys.glob("*png"))
files<-files[1:100]
for (i in seq_along(names)){
    
  fname<-sample(files)[1]
  m<-readPNG(fname, native = FALSE, info = FALSE)
  
  png(paste0("proppics/", names[i], ".png"), width=225, height=225)
  par(mar=c(0, 0, 0, 0), las=1)
  plot(0, type='n', xlim=0:1, ylim=0:1,xaxt = 'n', yaxt = 'n', bty = 'n', pch = '', ylab = '', xlab = '',
       cex.main=4)
  rasterImage(m, 0, 0, 1, 1)
  dev.off()
}

for (i in seq_along(names)){
  m<-readPNG(paste0(names[i], '.png'), native = FALSE, info = FALSE)
  
  png(paste0("inventpic/",names[i], '.png'), width=300, height=300)
  par(mar=c(2, 0, 0, 0), las=1)
  plot(0, type='n', xlim=0:1, ylim=0:1,xaxt = 'n', yaxt = 'n', bty = 'n', pch = '', ylab = '', xlab = '',
       cex.main=4)
  rasterImage(m, 0, 0, 1, 1)
  title(names[i], adj = 0.5, line = -20.7, cex.main=4)
  dev.off()
  
}