import subprocess
import sys

def test_warehouse_setup_runs():
    res = subprocess.run([sys.executable, "src/warehouse_setup.py"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Initialized Star Schema Warehouse" in res.stdout

def test_agent_executes_analytical_queries():
    res = subprocess.run([sys.executable, "src/agent.py"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Hyderabad" in res.stdout
    assert "Warm LED Chandelier" in res.stdout
