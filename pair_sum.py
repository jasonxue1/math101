from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass
from collections.abc import Iterable
from typing import cast

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from tqdm.rich import tqdm

import warnings

warnings.filterwarnings("ignore", message=".*rich is experimental/alpha.*")

console = Console()


def count_quadruples_pair_sum(
    target_sum: int,
    upper_bound: int,
    show_progress: bool = True,
    *,
    progress_position: int | None = None,
    progress_desc: str | None = None,
) -> int:
    """使用 pair-sum 计数表以 O(m^2) 时间统计满足 a<b<c<d<=upper_bound 且 a+b+c+d=target_sum 的四元组数量。"""
    if target_sum < 10 or target_sum > 4 * upper_bound - 6:
        return 0

    pair_counts: list[int] = [0] * (2 * upper_bound + 1)
    total = 0

    indices: Iterable[int]
    base_range = range(upper_bound - 2, 1, -1)
    if show_progress:
        indices = tqdm(
            base_range,
            desc=progress_desc or "Sweeping b",
            leave=False,
            dynamic_ncols=True,
            position=progress_position,
        )
    else:
        indices = base_range

    for second in indices:
        third = second + 1
        for fourth in range(third + 1, upper_bound + 1):
            pair_counts[third + fourth] += 1

        sum_without_first = target_sum - second
        for first in range(1, second):
            target = sum_without_first - first
            if 0 <= target <= 2 * upper_bound:
                total += pair_counts[target]

    return total


def pretty_print(
    target_sum: int, upper_bound: int, answer: int, elapsed: float
) -> None:
    """输出统计结果，包括参数、复杂度与运行耗时。"""
    header = Panel.fit(
        f"[bold cyan]a<b<c<d≤{upper_bound}, a+b+c+d={target_sum} 的解数[/bold cyan]",
        border_style="cyan",
    )
    console.print(header)

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("参数", justify="right", style="bold")
    table.add_column("值", justify="left")
    table.add_row("n", str(target_sum))
    table.add_row("m", str(upper_bound))
    table.add_row("复杂度", "时间 O(m²) / 空间 O(m)")
    table.add_row("结果", f"[bold green]{answer}[/bold green]")
    table.add_row("耗时", f"{elapsed:.3f} s")
    console.print(table)


@dataclass
class Arguments:
    """命令行参数的类型化表示。"""

    target_sum: int
    upper_bound: int
    no_progress: bool


def parse_args() -> Arguments:
    """解析命令行参数并返回类型化的结果。"""
    parser = ArgumentParser(
        description="Count quadruples with a<b<c<d<=m and a+b+c+d=n using an O(m^2) algorithm."
    )
    _ = parser.add_argument("n", type=int, help="目标和 n")
    _ = parser.add_argument("m", type=int, help="上界 m (d ≤ m)")
    _ = parser.add_argument("--no-progress", action="store_true", help="禁用进度条输出")
    parsed = parser.parse_args()

    return Arguments(
        target_sum=cast(int, parsed.n),
        upper_bound=cast(int, parsed.m),
        no_progress=cast(bool, parsed.no_progress),
    )


def main():
    target_sum, max_value = 10000, 20000
    print(count_quadruples_pair_sum(target_sum, max_value))


if __name__ == "__main__":
    main()
