# 🐱 Feline

**Decorator-based logging for Python — functions, methods, and entire classes.**

Feline wraps your callables with structured, rotating log output so you can track calls, execution time, and exceptions without cluttering your business logic.

---

## Features

- Log function calls, return times, and exceptions via simple decorators
- Separate loggers for plain functions, class methods, and entire classes
- Rotating file handler with configurable size and backup count
- Console output automatically disabled in frozen/production builds
- Dual-use decorators — use bare or with arguments

---

## Installation

```bash
pip install feline
```

> Requires Python 3.10+

---

## Quick Start

```python
from feline import FuncLogger, DEBUG

logger = FuncLogger(name="myapp", log_level=DEBUG)

@logger.debug
def fetch_data(url: str):
    ...

@logger.info(enabled=False)
def noisy_function():
    ...
```

---

## Loggers

### `FuncLogger` — standalone functions

```python
from feline import FuncLogger

logger = FuncLogger(name="player")

@logger.info
def load_track(path: str):
    ...

@logger.error(enabled=True)
def risky_operation():
    ...
```

### `MethodLogger` — individual class methods

Logs the class name alongside the method name (`MyClass.my_method called`).

```python
from feline import MethodLogger

logger = MethodLogger(name="ui")

class AudioPlayer:
    @logger.debug
    def play(self):
        ...

    @logger.warning
    def seek(self, position: int):
        ...
```

### `ClassLogger` — entire class at once(Currently not implemented)

Wraps every public method automatically.

```python
from feline import ClassLogger

logger = ClassLogger(name="storage")

@logger.info
class Database:
    def save(self, record): ...
    def fetch(self, id): ...
    def delete(self, id): ...
```

---

## Decorator Levels

Each logger exposes these decorator methods:

| Method | Log Level |
|--------|-----------|
| `.debug` | `DEBUG` (10) |
| `.info` | `INFO` (20) |
| `.warning` | `WARNING` (30) |
| `.error` | `ERROR` (40) |
| `.critical` | `CRITICAL` (50) |
| `.log` | `DEBUG` — general purpose |

All support the dual-use pattern:

```python
@logger.info              # bare — no arguments
def foo(): ...

@logger.info(enabled=False)   # with arguments
def bar(): ...
```

---

## Configuration

All loggers share the same constructor parameters:

```python
FuncLogger(
    name="myapp",           # logger name
    log_level=logging.INFO, # minimum level to capture
    filename="app.log",     # log file name
    max_bytes=5*1024*1024,  # 5 MB before rotation
    backup_count=5,         # rotated files to keep
    console=True,           # print to stdout
    log_dir="logs",         # directory for log files
    time_tracking=True,     # log execution duration
)
```

Console output is automatically disabled when the app is frozen (e.g. PyInstaller builds).

---

## Log Format

```
2026-03-25 14:32:01 | INFO     | player | load_track called
2026-03-25 14:32:01 | INFO     | player | load_track finished in 0.0031s
2026-03-25 14:32:05 | ERROR    | player | load_track raised after 0.0012s
```

---

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
