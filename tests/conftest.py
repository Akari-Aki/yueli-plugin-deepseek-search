"""把宿主源码加入用例路径，并禁止离线用例访问真实 HTTP 传输层。"""

from pathlib import Path

import httpx
import os
import pytest
import sys

YUELI_ROOT = Path(os.environ.get('YUELI_ROOT', 'D:/YueLiBot')).resolve()
sys.path.insert(0, str(YUELI_ROOT))


@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    """任何遗漏 MockTransport 的请求立即失败。"""
    async def forbidden(*_args, **_kwargs):
        raise AssertionError('离线用例禁止真实网络请求')

    monkeypatch.setattr(httpx.AsyncHTTPTransport, 'handle_async_request', forbidden)
