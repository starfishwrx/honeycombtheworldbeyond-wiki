import subprocess
import os

env = os.environ.copy()
env['HTTP_PROXY'] = 'http://127.0.0.1:7890'
env['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

cmd = [
    'cmd.exe', '/c',
    'codex', 'exec',
    '--dangerously-bypass-approvals-and-sandbox',
    'Use the cloudflare MCP server to list all DNS records for honeycombtheworldbeyond.wiki and update each of them so proxied is true.'
]

print("[INFO] Running codex exec...")
p = subprocess.Popen(
    cmd,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    env=env,
    text=True
)

try:
    stdout, _ = p.communicate(timeout=60)
    print("[OUTPUT]")
    print(stdout)
except subprocess.TimeoutExpired:
    p.kill()
    print("[TIMEOUT] Process timed out after 60s")
