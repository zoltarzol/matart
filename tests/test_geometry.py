import subprocess, sys

def test_cli_smoke():
    cmd = [
        sys.executable,
        "-m", "matart.geometry"
    ]
    output = subprocess.check_output(cmd).decode()
    assert "Generated shape:" in output
