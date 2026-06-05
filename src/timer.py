import time
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn

console = Console()

def focus_timer(minutes):
    seconds = minutes * 60
    start_time = time.time()
    
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        "/",
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[green]专注中...", total=seconds)
        
        while not progress.finished:
            elapsed = time.time() - start_time
            remaining = max(0, seconds - elapsed)
            progress.update(task, completed=seconds - remaining)
            time.sleep(0.1)
    
    console.print(f"\n[bold green]专注完成！[/bold green]共专注了 {minutes} 分钟")
    return minutes
