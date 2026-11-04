# 使い方: python3 turns.py "1つ目の文" "/compact" "3つ目の文"
# claude -p に1つずつ送り、返事（result）が来てから次を送る。返事の文字だけを出す。
import json, subprocess, sys
p = subprocess.Popen(["claude", "-p", "--input-format", "stream-json",
                      "--output-format", "stream-json", "--verbose"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
for i, t in enumerate(sys.argv[1:], 1):
    p.stdin.write(json.dumps({"type": "user", "message": {"role": "user", "content": t}}, ensure_ascii=False) + "\n")
    p.stdin.flush()
    for line in p.stdout:
        d = json.loads(line)
        if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
            print(f"[{i}] (要約が起きた)")
        if d.get("type") == "result":
            print(f"[{i}] {d.get('result', '')}")
            break
p.stdin.close(); p.wait()
