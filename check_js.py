# -*- coding: utf-8 -*-
import subprocess
import os

html_path = r"G:\我的雲端硬碟\0_AI Agent\Obsidian\DavidCloud\大衛人生\B3. 健康養生\B3.1 精力體態\energy-plan-4w\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

s_start = content.find("<script>")
s_end = content.find("</script>")
js_code = content[s_start+8:s_end]

temp_js = os.path.join(os.path.dirname(html_path), "temp_check.js")
with open(temp_js, "w", encoding="utf-8") as f:
    f.write(js_code)

print("Saved JS code, checking node syntax...")
res = subprocess.run(["node", "-c", temp_js], capture_output=True, text=True)
print("Node -c Return Code:", res.returncode)
print("Node stdout:", res.stdout)
print("Node stderr:", res.stderr)
