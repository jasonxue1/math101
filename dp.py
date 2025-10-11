from collections.abc import Iterable

from tqdm.rich import tqdm

import warnings

warnings.filterwarnings("ignore", message=".*rich is experimental/alpha.*")


def count_quadruples(
    target_sum: int,
    max_value: int,
    *,
    show_progress: bool = True,
    progress_position: int | None = None,
    progress_desc: str | None = None,
) -> int:
    """使用动态规划统计所有 1<=a<b<c<d<=max_value 且 a+b+c+d 等于 target_sum 的四元组数量。"""
    if target_sum < 10 or target_sum > 4 * max_value - 6:
        return 0

    count_table = [[0] * (target_sum + 1) for _ in range(5)]
    count_table[0][0] = 1

    iterator: Iterable[int]
    if show_progress:
        iterator = tqdm(
            range(1, max_value + 1),
            desc=progress_desc or "Processing numbers",
            unit="num",
            dynamic_ncols=True,
            leave=False,
            position=progress_position,
        )
    else:
        iterator = range(1, max_value + 1)

    for candidate in iterator:
        for numbers_selected in range(4, 0, -1):
            for current_sum in range(target_sum, candidate - 1, -1):
                count_table[numbers_selected][current_sum] += count_table[
                    numbers_selected - 1
                ][current_sum - candidate]

    return count_table[4][target_sum]


def main():
    target_sum, max_value = 10000, 20000
    print(count_quadruples(target_sum, max_value))


if __name__ == "__main__":
    main()
