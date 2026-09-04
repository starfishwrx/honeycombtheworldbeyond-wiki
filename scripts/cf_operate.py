import json
import subprocess
import urllib.request
import urllib.parse
import sys

def get_token():
    ps_cmd = """
    Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;
    using System.Text;
    public class CredReader {
        [DllImport("advapi32.dll", EntryPoint = "CredReadW", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern bool CredRead(string target, int type, int reservedFlag, out IntPtr credentialPtr);
        [DllImport("advapi32.dll", SetLastError = true)]
        public static extern void CredFree(IntPtr credentialPtr);
        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
        public struct CREDENTIAL {
            public int Flags;
            public int Type;
            public string TargetName;
            public string Comment;
            public long LastWritten;
            public int CredentialBlobSize;
            public IntPtr CredentialBlob;
            public int Persist;
            public int AttributeCount;
            public IntPtr Attributes;
            public string TargetAlias;
            public string UserName;
        }
        public static string Read(string target) {
            IntPtr ptr;
            if (CredRead(target, 1, 0, out ptr)) {
                CREDENTIAL cred = (CREDENTIAL)Marshal.PtrToStructure(ptr, typeof(CREDENTIAL));
                byte[] blob = new byte[cred.CredentialBlobSize];
                Marshal.Copy(cred.CredentialBlob, blob, 0, cred.CredentialBlobSize);
                CredFree(ptr);
                return Encoding.Unicode.GetString(blob);
            }
            return null;
        }
    }
"@ -ErrorAction SilentlyContinue
    [CredReader]::Read("cloudflare-api|2e40c71145c8b601.Codex MCP Credentials")
    """
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout.strip():
        raise RuntimeError("Failed to read credential from Windows Credential Manager")
    data = json.loads(res.stdout.strip())
    token = data["token_response"]["access_token"]
    return token

def main():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Get Zone ID
    zone_name = "honeycombtheworldbeyond.wiki"
    url = f"https://api.cloudflare.com/client/v4/zones?name={zone_name}"
    req = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'https': 'http://127.0.0.1:7890'}))
    
    with opener.open(req) as resp:
        result = json.loads(resp.read().decode())
    
    if not result.get("success") or not result.get("result"):
        print(f"[ERROR] Zone {zone_name} not found in Cloudflare: {result}")
        return 1
        
    zone = result["result"][0]
    zone_id = zone["id"]
    print(f"[OK] Found Zone: {zone_name} (ID: {zone_id}, Status: {zone['status']})")
    
    # 2. Get DNS Records
    dns_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    req = urllib.request.Request(dns_url, headers=headers)
    with opener.open(req) as resp:
        dns_result = json.loads(resp.read().decode())
        
    records = dns_result.get("result", [])
    print(f"[OK] Found {len(records)} DNS records:")
    for r in records:
        print(f"  - {r['type']} {r['name']} -> {r['content']} (Proxied: {r['proxied']}) [ID: {r['id']}]")
        
    # 3. Update records to proxied: true
    for r in records:
        if r["type"] in ("A", "AAAA", "CNAME") and not r["proxied"]:
            update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{r['id']}"
            update_body = json.dumps({
                "type": r["type"],
                "name": r["name"],
                "content": r["content"],
                "proxied": True,
                "ttl": 1 # Automatic TTL when proxied
            }).encode()
            req = urllib.request.Request(update_url, data=update_body, headers=headers, method="PATCH")
            try:
                with opener.open(req) as resp:
                    res_json = json.loads(resp.read().decode())
                    if res_json.get("success"):
                        print(f"[SUCCESS] Updated {r['name']} to PROXIED (Orange Cloud enabled!)")
                    else:
                        print(f"[WARN] Failed to update {r['name']}: {res_json}")
            except urllib.error.HTTPError as err:
                print(f"[ERROR] HTTP {err.code}: {err.read().decode()}")

if __name__ == "__main__":
    main()
