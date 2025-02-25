from utttai_conversion.utttai_convert import utttai_small_index_to_u3t_small_index, u3t_to_utttai
import timeit
import random

def time_conversion(test_nums: list[int]):
    for num in test_nums:
        utttai_small_index_to_u3t_small_index(num)
        u3t_to_utttai(num)

def time_lookup(test_nums: list[int], u3t_to_utttai: dict[int, int], utttai_to_u3t: dict[int, int]):
    for num in test_nums:
        u3t_to_utttai[num]
        utttai_to_u3t[num]
def compare_speed_to_lookup():
    u3t_to_utttai = {
        0: 60, 1: 61, 2: 62, 3: 69, 4: 70, 5: 71, 6: 78, 7: 79, 8: 80,
        9: 57, 10: 58, 11: 59, 12: 66, 13: 67, 14: 68, 15: 75, 16: 76, 17: 77,
        18: 54, 19: 55, 20: 56, 21: 63, 22: 64, 23: 65, 24: 72, 25: 73, 26: 74,
        27: 33, 28: 34, 29: 35, 30: 42, 31: 43, 32: 44, 33: 51, 34: 52, 35: 53,
        36: 30, 37: 31, 38: 32, 39: 39, 40: 40, 41: 41, 42: 48, 43: 49, 44: 50,
        45: 27, 46: 28, 47: 29, 48: 36, 49: 37, 50: 38, 51: 45, 52: 46, 53: 47,
        54: 6, 55: 7, 56: 8, 57: 15, 58: 16, 59: 17, 60: 24, 61: 25, 62: 26,
        63: 3, 64: 4, 65: 5, 66: 12, 67: 13, 68: 14, 69: 21, 70: 22, 71: 23,
        72: 0, 73: 1, 74: 2, 75: 9, 76: 10, 77: 11, 78: 18, 79: 19, 80: 20
    }
    utttai_to_u3t = {v: k for k, v in u3t_to_utttai.items()}

    test_nums = [random.randint(0, 80) for _ in range(1000)]
    print("Speed test comparison")
    print("Conversion")
    print(timeit.timeit(lambda: time_conversion(test_nums), number=1000))
    print("Lookup")
    print(timeit.timeit(lambda: time_lookup(test_nums, u3t_to_utttai, utttai_to_u3t), number=1000))

if __name__ == '__main__':
    compare_speed_to_lookup()