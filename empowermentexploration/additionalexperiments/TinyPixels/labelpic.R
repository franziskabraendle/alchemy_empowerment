library(stringr)

setwd("/home/hanshalbe/ericschulz.github.io/TinyFractals/proppics/")

files <- (Sys.glob("*png"))

for (i in seq_along(files)){
  m<-readPNG(files[i], native = FALSE, info = FALSE)

  png(paste0("/home/hanshalbe/ericschulz.github.io/TinyFractals/inventpic/",files[i]), width=300, height=300)
  par(mar=c(2, 0, 0, 0), las=1)
  plot(0, type='n', xlim=0:1, ylim=0:1,xaxt = 'n', yaxt = 'n', bty = 'n', pch = '', ylab = '', xlab = '',
     cex.main=4)
  rasterImage(m, 0, 0, 1, 1)
  title(str_replace(files[i], ".png", ""), adj = 0.5, line = -20.7, cex.main=4)
  dev.off()
  
}

n<-names[1:length(files)]
paste0("'",paste0(n, sep="", collapse="','"),"'")
