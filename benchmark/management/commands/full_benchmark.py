from django.core.management.base import BaseCommand
from benchmark.utils import (
    drop_indexes,
    setup_indexes,
    optimize_schema,
    run_benchmarks,
)
from rich.console import Console

console = Console()


class Command(BaseCommand):
    help = "Run full benchmark with optimization"

    def handle(self, *args, **kwargs):
        console.rule("[bold blue]Benchmarking Before Optimization")
        drop_indexes()
        run_benchmarks()

        console.rule("[bold blue]Optimizing Schema & Indexes")
        optimize_schema()
        setup_indexes()

        console.rule("[bold blue]Benchmarking After Optimization")
        run_benchmarks()
