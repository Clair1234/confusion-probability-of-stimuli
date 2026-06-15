#HEADER

def normalize(matrix):
    normalized_matrix = {}
    for signal1 in matrix.keys():
        sum_on_column = compute_sum_cols(matrix, signal1)
        normalized_matrix[signal1] = {}
        for signal2 in matrix[signal1].keys():
            normalized_matrix[signal1][signal2] = matrix[signal1][signal2] / sum_on_column
            
    return normalized_matrix

def compute_sum_cols(matrix, row):
    val = 0
    for key in matrix[row].keys():
        val += matrix[row][key]
        
    return val 
