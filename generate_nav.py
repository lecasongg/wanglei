#!/usr/bin/env python3
"""扫描仓库中所有 .html 文件，自动生成 index.html 导航页面。"""
import os
import json
from pathlib import Path

REPO = Path(__file__).parent
INDEX = REPO / "index.html"
EXCLUDE = {".git", "__pycache__"}

ICON_MAP = {
    "公告": "📢",
    "通知": "🔔",
    "首页": "🏠",
    "关于": "ℹ️",
    "联系": "📞",
    "帮助": "❓",
    "文档": "📄",
    "设置": "⚙️",
    "登录": "🔑",
    "注册": "📝",
    "表单": "📋",
    "列表": "📑",
    "详情": "🔍",
    "编辑": "✏️",
    "管理": "📂",
    "报告": "📊",
    "分析": "📈",
    "图表": "📉",
    "配置": "🔧",
    "搜索": "🔎",
    "消息": "💬",
    "用户": "👤",
    "权限": "🔐",
    "日志": "📝",
    "导出": "📤",
    "导入": "📥",
    "数据": "🗃️",
    "错误": "⚠️",
    "成功": "✅",
    "失败": "❌",
    "默认": "📄",
}

def guess_icon(filename: str) -> str:
    """根据文件名猜测图标"""
    name = filename.replace(".html", "")
    for keyword, icon in ICON_MAP.items():
        if keyword in name:
            return icon
    return "📄"

def collect_html_files():
    """递归扫描所有 .html 文件，按目录归类"""
    pages = {}  # {directory: [(filename, relative_path), ...]}
    for html in sorted(REPO.rglob("*.html")):
        rel = html.relative_to(REPO)
        if any(part.startswith(".") or part in EXCLUDE for part in rel.parts):
            continue
        parent = str(rel.parent)
        if parent == ".":
            # index.html itself is excluded from the listing
            if html.name == "index.html":
                continue
            parent = "/"
        pages.setdefault(parent, []).append((html.name, str(rel.as_posix())))
    return pages

def build_html(pages: dict) -> str:
    """生成导航页面 HTML"""
    emoji_list = "".join(ICON_MAP.values())
    
    cards_html = ""
    for directory in sorted(pages.keys()):
        items = pages[directory]
        # Skip root index.html, already handled
        for name, path in items:
            display_name = name.replace(".html", "")
            icon = guess_icon(name)
            cards_html += f"""
        <div class="file-card">
            <div class="file-info">
                <div class="file-icon">{icon}</div>
                <div>
                    <div class="file-name">{display_name}</div>
                    <div class="file-path">{path}</div>
                </div>
            </div>
            <a class="btn" href="{path}" target="_blank">查看</a>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>王雷的网页管理入口</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f7fa;
            color: #333;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header .count {{ font-size: 14px; opacity: 0.85; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 24px 16px; }}
        .search-box {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-box:focus {{ border-color: #667eea; }}
        .section-title {{
            font-size: 16px;
            font-weight: 600;
            color: #555;
            margin: 24px 0 12px;
            padding-left: 12px;
            border-left: 3px solid #667eea;
        }}
        .file-card {{
            background: white;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s;
        }}
        .file-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            transform: translateY(-1px);
        }}
        .file-info {{ display: flex; align-items: center; gap: 12px; }}
        .file-icon {{
            width: 40px; height: 40px;
            background: #eef2ff;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px;
        }}
        .file-name {{ font-weight: 500; color: #333; }}
        .file-path {{ font-size: 12px; color: #999; margin-top: 2px; }}
        .btn {{
            padding: 6px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            background: #667eea;
            color: white;
            transition: background 0.2s;
            white-space: nowrap;
        }}
        .btn:hover {{ background: #5a6fd6; }}
        .empty {{
            text-align: center;
            padding: 60px 20px;
            color: #aaa;
        }}
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #aaa;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📂 王雷的网页管理入口</h1>
        <div class="count">共 {sum(len(v) for v in pages.values())} 个页面</div>
    </div>
    <div class="container">
        <input class="search-box" type="text" id="search" placeholder="🔎 搜索页面名称..." oninput="filterPages()">
        <div id="pageList">{cards_html}</div>
    </div>
    <div class="footer">新页面推送后自动更新</div>
    <script>
        function filterPages() {{
            const q = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.file-card').forEach(card => {{
                const name = card.querySelector('.file-name').textContent.toLowerCase();
                const path = card.querySelector('.file-path').textContent.toLowerCase();
                card.style.display = name.includes(q) || path.includes(q) ? 'flex' : 'none';
            }});
        }}
    </script>
</body>
</html>"""


def main():
    pages = collect_html_files()
    html = build_html(pages)
    INDEX.write_text(html, encoding="utf-8")
    total = sum(len(v) for v in pages.values())
    print(f"✅ 导航页已生成，共 {total} 个页面")

if __name__ == "__main__":
    main()
