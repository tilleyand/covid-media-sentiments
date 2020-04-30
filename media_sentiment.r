
library(rvest)
library(xml2)
library(stringr)

url <- "https://www.wsj.com/news/archive/20200428"
xx <- read_html(url)
xx_txt = html_text(xx)

xx_txt %>% str_locate_all("America Movil")
str_sub(xx_txt, 157490, 157600)

