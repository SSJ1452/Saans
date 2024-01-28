import pytest
from utils import vcr_kwargs


def pytest_addoption(parser):
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")



def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="skipped due to --skip-slow")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)



@pytest.fixture(scope="session")
def vcr_config():
    return vcr_kwargs
