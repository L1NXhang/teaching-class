# Binary Tree Micro-Lecture — Slides

《二叉树及其遍历》微课 — 高中信息技术 选择性必修 1 §3.5(人教版),共 22 张幻灯

## 用法

```bash
# 1. 启动一个静态服务器(任何方式都行)
python -m http.server 8080
# 或
npx serve .

# 2. 浏览器打开
open http://localhost:8080/
```

> ⚠️ 必须通过 HTTP 访问,直接双击 `index.html` 会有 CORS 限制。

## 键盘快捷键

| 键 | 作用 |
|----|------|
| `←` `→` / `Space` | 翻页 |
| `S` | 打开演讲者视图(独立窗口) |
| `N` | 底部抽屉显示逐字稿 |
| `O` | 全部幻灯总览 |
| `T` | 切换主题(memphis-pop / sunset-warm / engineering-whiteprint / academic-paper / solarized-light) |
| `F` | 全屏 |
| `?` | 显示/重置右下角快捷键提示 |

## 文件结构

```
binary-tree-lecture/
├── index.html                 20 张幻灯主文件
├── style.css                  主题与排版
├── textbook-cover.png         教材封面
└── assets/
    ├── base.css               重置 + 排版原语
    ├── fonts.css              字体声明
    ├── runtime.js             翻页 / 主题 / 演讲者视图 runtime
    ├── animations/
    │   └── animations.css     动画库
    └── themes/
        ├── memphis-pop.css          孟菲斯波普
        ├── sunset-warm.css          落日暖橙
        ├── engineering-whiteprint.css  工程白图
        ├── academic-paper.css       学术论文
        ├── solarized-light.css      Solarized 浅色
        ├── corporate-clean.css      商务净色(备用)
```

## 演讲者视图

按 `S` 打开独立窗口,带 4 张可拖动卡片:
- **CURRENT** — 当前幻灯的高保真预览
- **NEXT** — 下一张预览
- **SPEAKER SCRIPT** — 当前页逐字稿
- **TIMER** — 计时器 + 翻页控制

## 主题切换

按 `T` 循环切换 5 套主题。切换后会同时同步给演讲者窗口。
