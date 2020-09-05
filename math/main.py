import math

def getVariance(nums):
    i = 0
    variance = 0
    while i < 9:
        print(i)
        variance += (i - 3.12)*(i-3.12)*nums[i]
        i += 1
    print(variance)

def getMean(nums):
    mean = 0
    for num in nums:
        mean += num * (5*num/55)
    print(mean)
    variance = getVarianceMass(nums)
    variance = variance - mean * mean
    print(variance)


def getVarianceMass(nums):
    mean = 0
    for num in nums:
        mean += num * num *(5*num/55)
    print(mean)
    return mean

def main():
    nums = [0.1371,	0.2920,	0.1398,	0.0730,
            0.02929, 0.0730, 0.08959, 0.01993, 0.1460]
    # getVariance(nums)
    getMean([0,1,2,3,4])
    # getVarianceMass([0, 1, 2, 3, 4])
if __name__ == "__main__":
    main()
