def DCG(num):
    sum = 0
    for idx, val in enumerate(num):
        sum += val / (idx + 1)
    
    return sum

scores = [2, 2, 2, 1.5]

print(DCG(scores))
