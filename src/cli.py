import click
from datetime import date
from rich.console import Console
from rich.table import Table
from .timer import focus_timer
from .deepseek import generate_morning_sentence, generate_review_report
from .feishu import send_feishu_message, add_record_to_feishu_table
from .storage import update_focus_time, update_early_rise, update_review, get_today_record

console = Console()

@click.group()
def cli():
    """学习打卡 AI 智能体 - 助你高效学习每一天"""
    pass

@cli.command()
@click.option('--minutes', '-m', default=25, help='专注时长（分钟），默认25分钟')
@click.option('--task', '-t', default='通用', help='学习科目（数学/英语/专业课等）')
def focus(minutes, task):
    """启动专注计时器"""
    console.print(f"[bold blue]开始 {task} 专注计时（{minutes} 分钟）...[/bold blue]")
    focus_time = focus_timer(minutes)
    update_focus_time(focus_time, task)
    console.print("[bold green]专注时长已记录！[/bold green]")

@cli.command()
def morning():
    """发送早安推送与每日一句"""
    console.print("[bold blue]正在生成今日佳句...[/bold blue]")
    sentence = generate_morning_sentence()
    
    if "失败" in sentence:
        console.print(f"[bold red]生成失败：{sentence}[/bold red]")
        return
    
    console.print(f"\n[bold green]今日佳句：[/bold green]")
    console.print(sentence)
    
    console.print("\n[bold blue]正在发送到飞书...[/bold blue]")
    success, msg = send_feishu_message(f"🌅 早安！今日佳句：\n{sentence}")
    
    if success:
        console.print("[bold green]消息发送成功！[/bold green]")
        update_early_rise()
        console.print("[bold green]早起打卡已记录！[/bold green]")
    else:
        console.print(f"[bold red]发送失败：{msg}[/bold red]")

@cli.command()
def review():
    """生成晚间复盘报告"""
    today = date.today().strftime("%Y-%m-%d")
    record = get_today_record()

    if not record:
        console.print("[bold yellow]今日暂无学习记录[/bold yellow]")
        focus_time = 0
        early_rise = "否"
        focus_data = {}
    else:
        focus_data = record.get("专注数据", {})
        focus_time = record.get("专注时长", 0)
        early_rise = record.get("早起状态", "否")

    console.print("[bold blue]正在生成复盘报告...[/bold blue]")
    report = generate_review_report(today, focus_time, early_rise, focus_data)
    
    if "失败" in report:
        console.print(f"[bold red]生成失败：{report}[/bold red]")
        return
    
    console.print(f"\n[bold green]📝 今日复盘报告：[/bold green]")
    console.print(report)
    
    console.print("\n[bold blue]正在发送到飞书...[/bold blue]")
    success, msg = send_feishu_message(f"📝 今日复盘报告：\n{report}")
    
    if success:
        console.print("[bold green]消息发送成功！[/bold green]")
        update_review(report)
        console.print("[bold green]复盘报告已保存！[/bold green]")
    else:
        console.print(f"[bold red]发送失败：{msg}[/bold red]")

@cli.command()
def status():
    """查看今日学习状态"""
    record = get_today_record()

    if not record:
        console.print("[bold yellow]今日暂无学习记录[/bold yellow]")
        return

    table = Table(title="📊 今日学习状态")
    table.add_column("项目", style="cyan")
    table.add_column("状态", style="green")

    table.add_row("日期", record["日期"])
    table.add_row("早起状态", record["早起状态"])

    focus_data = record.get("专注数据", {})
    if focus_data:
        for task, minutes in focus_data.items():
            table.add_row(f"专注-{task}", f"{minutes} 分钟")
    else:
        table.add_row("专注时长", "0 分钟")

    total = record.get("专注时长", 0)
    table.add_row("专注时长（总计）", f"{total} 分钟")

    review = record.get("复盘总结", "")
    if review:
        table.add_row("复盘状态", "已完成")
    else:
        table.add_row("复盘状态", "待完成")

    console.print(table)

if __name__ == "__main__":
    cli()
