from functools import wraps
from math import comb
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

from rich.console import Console
from rich.table import Table
from tqdm.rich import tqdm

from dp import count_quadruples as count_with_upper_bound
from pair_sum import count_quadruples_pair_sum

import warnings

warnings.filterwarnings("ignore", message=".*rich is experimental/alpha.*")

P = ParamSpec("P")
R = TypeVar("R")


def timed(func: Callable[P, R]) -> Callable[P, tuple[R, float]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[R, float]:
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        return result, elapsed

    return wrapper


@timed
def solve_with_formula(n: int) -> int:
    """使用组合数学推导计算满足 1<=a<b<c<d<=n 且 a+b+c+d 可被 n 整除的四元组数量。"""
    if n < 5:
        return 0

    base = comb(n, 4) * 4 // n  # 基础项（t=0的贡献）

    match n % 4:
        case 1 | 3:
            return base // 4
        case 2:
            return (base * 2 + n - 2) // 8
        case 0:
            return (base * 2 + n - 6) // 8
        case _:
            return 0


@timed
def solve_with_dp(
    n: int,
    *,
    show_progress: bool = False,
    progress_position: int | None = None,
    progress_desc: str | None = None,
) -> int:
    """通过调用动态规划求解器累加满足条件的四元组数量。"""
    return sum(
        count_with_upper_bound(
            n * multiplier,
            n,
            show_progress=show_progress,
            progress_position=progress_position,
            progress_desc=(
                f"{progress_desc} (mult={multiplier})" if progress_desc else None
            ),
        )
        for multiplier in (1, 2, 3)
    )


@timed
def solve_with_pair_sum(
    n: int,
    *,
    show_progress: bool = False,
    progress_position: int | None = None,
    progress_desc: str | None = None,
) -> int:
    """通过 pair-sum 算法累加满足条件的四元组数量。"""
    return sum(
        count_quadruples_pair_sum(
            n * multiplier,
            n,
            show_progress=show_progress,
            progress_position=progress_position,
            progress_desc=(
                f"{progress_desc} (mult={multiplier})" if progress_desc else None
            ),
        )
        for multiplier in (1, 2, 3)
    )


if __name__ == "__main__":
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 101, 303, 384, 390, 505, 676, 888, 1024]
    console = Console()
    table = Table(title="Quadruple Counts", header_style="bold")
    table.add_column("n", justify="right")
    table.add_column("公式结果", justify="right")
    table.add_column("公式耗时(s)", justify="right")
    table.add_column("DP结果", justify="right")
    table.add_column("DP耗时(s)", justify="right")
    table.add_column("Pair结果", justify="right")
    table.add_column("Pair耗时(s)", justify="right")

    mismatches: list[int] = []

    with tqdm(
        total=len(lst),
        desc="总进度",
        unit="n",
        dynamic_ncols=True,
        position=0,
    ) as total_bar:
        for n in lst:
            formula_result, formula_time = solve_with_formula(n)
            dp_result, dp_time = solve_with_dp(
                n,
                show_progress=True,
                progress_position=1,
                progress_desc=f"DP n={n}",
            )
            pair_result, pair_time = solve_with_pair_sum(
                n,
                show_progress=True,
                progress_position=1,
                progress_desc=f"Pair n={n}",
            )

            table.add_row(
                str(n),
                str(formula_result),
                f"{formula_time:.6f}",
                str(dp_result),
                f"{dp_time:.6f}",
                str(pair_result),
                f"{pair_time:.6f}",
            )

            if len({formula_result, dp_result, pair_result}) != 1:
                mismatches.append(n)

            _ = total_bar.update(1)

    if mismatches:
        mismatch_message = ", ".join(str(n) for n in mismatches)
        console.print(
            f"[bold red]Warning:[/bold red] Results differ for n={mismatch_message}."
        )

    console.print(table)
