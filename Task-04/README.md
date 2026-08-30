## approach

### 1. digitstring

first i took the number of test cases and then read the string. i counted the number of `1` and `3` in the string first. after that i went through the string again and kept updating the count when i found `2`, while reducing the count of `1` and `3`. i used `math.max` to keep the best value found and finally printed the length of the string minus that value.

### 2. duck

first i read the number of elements and stored them in an array. i used a loop to compare the current element with the previous one and swapped them if they were in the wrong order. while doing this i also added the values based on the comparison. after the sorting was done, i printed the last element of the array.

### 3. good number

i made a function `count()` to find how many digits are there in a number. for every input number, i used this count to find the required power of `10` and then added `1` to it. this value is then printed for each number.

### 4. papyrus

first i took the two arrays as input and checked if the first array is already smaller than the second one at any position. i also calculated the value if no reordering is done. then i sorted both arrays and checked again if the sorted arrays can satisfy the condition. based on these conditions, i printed `-1`, the original value, or the smaller value between the two possible results.
