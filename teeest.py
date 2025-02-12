from rich.console import Console
from rich.table import Table
from rich import box

table = Table(title="===== Задачи =====", expand=True)

table.add_column("№", justify="right", style="cyan")
table.add_column("Название", style="white")
table.add_column("Дедлайн", justify="right", style="green")

table.add_row("1", "Сдать проект", "2025-02-09 19:00:00")
table.add_row("2", "Написать злостную гиперматику", "2025-02-12 19:00:00")

console = Console()
console.print(table)