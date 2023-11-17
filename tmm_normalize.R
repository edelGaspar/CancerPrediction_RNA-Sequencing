

# Leer el archivo CSV de expresiones genéticas
ruta_archivo <- "D:/DataScience_and_Python/Magister IA VIU/TFM/Desarrollo/Data/IntVeld2022/TEP_Count_Matrix.tsv"


## Load the library edgeR
library(edgeR)

#Read the file with read counts

counts <- read.table(ruta_archivo, sep = "\t", header = TRUE, row.names = 1, check.names = FALSE)

# Convert Null values to 0
counts[is.na(counts)] <- 0

#samples_names <- colnames(counts)

# Give condition to each column (samples) in the counts
#group <- factor (c(1,1,1,1,2,2,2,2,3,3,3,3))


y <- DGEList(counts=counts)

## normalize using TMM
y <- calcNormFactors (y, method="TMM")

## obtain normalized data on the log2-scale
logCPMs <- cpm(y, log = TRUE, normalized.lib.sizes = T)

#colnames(logCPMs) <- samples_names

ruta_salida <- "D:/DataScience_and_Python/Magister IA VIU/TFM/Desarrollo/Data/IntVeld2022/TEP_Count_Matrix_tmm.csv"

write.table(logCPMs,file= ruta_salida, sep="\t", row.names = T,col.names = T,quote = F)



