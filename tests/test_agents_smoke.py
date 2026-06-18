# from __future__ import annotations: 启用延迟注解求值（Python 3.7+）
# 允许前向引用类型注解，减少运行时开销（类似 Java 的编译时类型擦除）
from __future__ import annotations

from pathlib import Path
import py_compile  # Python 编译检查（类似 javac -Xlint 语法检查）

import pytest  # pytest 测试框架（类似 Java 的 JUnit 5 + AssertJ）


# Path(__file__).resolve().parents[1] 定位项目根目录
# __file__ 是当前文件路径（类似 Java 的 getClass().getProtectionDomain().getCodeSource()）
# .parents[1] 取父目录的父目录（类似 Path.getParent().getParent()）
ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
# 列表推导式：收集所有 agent 文件，排除 __init__.py
AGENT_FILES = sorted(
    path for path in AGENTS_DIR.glob("*.py") if path.name != "__init__.py"
)
AGENT_IDS = [path.name for path in AGENT_FILES]


# @pytest.mark.parametrize 参数化测试（类似 JUnit 5 @ParameterizedTest + @MethodSource）
# 为每个 agent 文件生成独立的测试用例
@pytest.mark.parametrize("agent_path", AGENT_FILES, ids=AGENT_IDS)
def test_agent_scripts_compile(agent_path: Path) -> None:
    # py_compile.compile() 编译检查 Python 文件语法（类似 javac 编译检查）
    # doraise=True: 编译失败时抛出异常（类似 failOnError）
    _ = py_compile.compile(str(agent_path), doraise=True)


def test_agent_scripts_exist() -> None:
    # assert 断言（类似 Java 的 assertTrue / assertEquals）
    # pytest 失败时会显示表达式的实际值
    assert AGENT_FILES, "expected at least one agent script"
