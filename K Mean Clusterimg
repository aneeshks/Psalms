rm(list=ls())

require(plyr)

Get.Distance <- function(x, centers) {
  n <- nrow(x)
  k <- nrow(centers)
  dist <- matrix(0, n, k)
  for (i in 1:n){
    for (j in 1:k){
      dist[i,j] <- sqrt(sum((x[i,-ncol(x)] - centers[j,])^2))
    }
  }
  return(dist)
}

My.Means <- function(x) {
  tmp <- ddply(x, .(labels), function(g){colMeans(g)})
  return(tmp[,-ncol(x)])
}  

My.Kmeans <- function(x, centers, max.iter, nstart) {
  centers <- x[sample(1:nrow(x), centers), ]
  x$labels <- 1:nrow(centers)
  
  for (i in 1:max.iter) {
    dist <- Get.Distance(x, centers)
    x$labels <- apply(dist, 1, which.min)
    centers <- My.Means(x)
  }
  
  return(list(clusters=x$labels, centers=centers))
}
