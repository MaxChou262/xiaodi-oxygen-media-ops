# HTML 交付规范：一个文件，能看、能念、能打印

经销商不是坐电脑前读稿的人。他站在舱边上，一只手拿手机，另一只手要去调压力表。
所以这份 HTML 要在三种场景下都不难看：**手机竖屏、电脑浏览器、打印成 PDF。**

下面这套是定稿版式。**照抄骨架，只换内容**——不要每次自己发明配色和间距，经销商拿到手的感觉必须稳定，像同一家店出的东西。

---

## 一、三条硬约束

| 约束 | 原因 |
|---|---|
| 单文件、样式内联、零外链 | 店里网络差，发微信要能直接打开。外链字体一断就变宋体乱版 |
| 手机竖屏优先 | 90% 的打开场景是手机。桌面好看手机难看，等于没做 |
| 口播可一键复制 | 他要粘到提词器或剪映里。让他手选一段文字，就会漏字 |

禁用：外链字体、CDN 图标库、需要联网的图片、emoji 当图标、徽标里的「✨🚀」这类装饰。

---

## 二、设计变量

| 项 | 值 | 说明 |
|---|---|---|
| 正文色 | `#1b1b1b` | 不用纯黑，手机上看不刺眼 |
| 次文色 | `#6d6a64` | 说明文字、元信息 |
| 强调色 | `#a9791f` | 暖金，只用在编号、徽标、关键数字。**全页只有这一个彩色** |
| 页面底 | `#ffffff` | |
| 卡片底 | `#fbf8f2` | 比页面略暖，卡片才能浮起来 |
| 描边 | `#e7e0d3` | 1px，别加阴影，打印会糊 |
| 正文字号 | `16px`（手机 `15px`） | 小于 15px 在阳光下看不清 |
| 行高 | `1.8`（口播区 `1.95`） | 口播要大行高，方便手指点着念 |
| 圆角 | `10px` | 不要全圆角，太像消费类 App |

字体栈（系统字体，零加载）：

```css
font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
             "HarmonyOS Sans SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
```

数字与编号用等宽感字体，制造「表格感」：

```css
font-family: ui-monospace, "SF Mono", Consolas, "Courier New", monospace;
```

---

## 三、完整骨架（复制即用）

把 `{{...}}` 换成内容，其余不动。**这份骨架就是验收标准。**

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>小狄氧舱 · {{城市}} · {{型号}} · {{YYYY-MM-DD}}</title>
<style>
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{
    margin:0;padding:28px 20px 56px;background:#fff;color:#1b1b1b;
    font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","HarmonyOS Sans SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;
    font-size:16px;line-height:1.8;
  }
  .wrap{max-width:760px;margin:0 auto}

  /* 顶栏 */
  .kicker{font-size:12px;letter-spacing:.14em;color:#a9791f;text-transform:uppercase;margin:0 0 10px}
  h1{font-size:26px;line-height:1.35;margin:0 0 14px;font-weight:650;letter-spacing:-.01em}
  .meta{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}
  .pill{font-size:12.5px;color:#4a4640;background:#fbf8f2;border:1px solid #e7e0d3;
        border-radius:999px;padding:3px 11px;font-family:ui-monospace,Consolas,monospace}
  .pill.hot{color:#8a5f12;border-color:#e3cf9e;background:#fdf6e6}
  .lede{font-size:14.5px;color:#6d6a64;margin:0 0 22px;padding-left:12px;border-left:2px solid #e7e0d3}

  /* 区块标题 */
  h2{font-size:14px;letter-spacing:.1em;color:#8a8478;font-weight:600;
     margin:34px 0 12px;padding-bottom:8px;border-bottom:1px solid #e7e0d3}

  /* 热点区 */
  .hots{list-style:none;margin:0;padding:0}
  .hots li{position:relative;padding:9px 0 9px 26px;font-size:15px;border-bottom:1px dashed #f0eade}
  .hots li:last-child{border-bottom:0}
  .hots li::before{content:attr(data-i);position:absolute;left:0;top:10px;
    font-family:ui-monospace,Consolas,monospace;font-size:12px;color:#a9791f}
  .hots .src{display:block;font-size:12.5px;color:#8a8478;margin-top:2px}

  /* 脚本卡 */
  .card{background:#fbf8f2;border:1px solid #e7e0d3;border-radius:10px;
        padding:20px 20px 16px;margin:0 0 18px}
  .head{display:flex;align-items:baseline;gap:12px;margin:0 0 6px}
  .num{font-family:ui-monospace,Consolas,monospace;font-size:24px;line-height:1;
       color:#a9791f;font-weight:600;letter-spacing:-.02em}
  .head h3{font-size:18px;line-height:1.45;margin:0;font-weight:640;flex:1}
  .type{font-size:11.5px;color:#6d6a64;border:1px solid #e7e0d3;background:#fff;
        border-radius:4px;padding:1px 7px;white-space:nowrap}
  .hot-line{font-size:13px;color:#6d6a64;margin:0 0 14px;padding-left:36px}

  /* 口播区 */
  .vo{background:#fff;border:1px solid #ece5d8;border-radius:8px;padding:14px 16px 10px}
  .vo-bar{display:flex;align-items:center;justify-content:space-between;
          gap:10px;margin:0 0 8px}
  .vo-bar span{font-size:12.5px;color:#8a8478;font-family:ui-monospace,Consolas,monospace}
  .copy{font:inherit;font-size:12.5px;color:#8a5f12;background:#fdf6e6;
        border:1px solid #e3cf9e;border-radius:5px;padding:3px 10px;cursor:pointer}
  .copy:active{transform:translateY(1px)}
  .vo p{font-size:17px;line-height:1.95;margin:0 0 12px;letter-spacing:.01em}
  .vo p:last-child{margin-bottom:4px}

  /* 镜头与元信息 */
  .shots{list-style:none;margin:14px 0 0;padding:0;counter-reset:s}
  .shots li{counter-increment:s;position:relative;padding-left:24px;
            font-size:14.5px;color:#3d3a34;margin-bottom:5px}
  .shots li::before{content:"镜" counter(s);position:absolute;left:0;top:1px;
    font-size:11.5px;color:#a9791f;font-family:ui-monospace,Consolas,monospace}
  .foot{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0 0;padding-top:12px;
        border-top:1px solid #ece5d8;font-size:12.5px;color:#8a8478}
  .cta{font-size:14px;margin:10px 0 0;color:#3d3a34}
  .cta b{color:#8a5f12;font-weight:600}

  /* 页脚 */
  .end{margin:40px 0 0;padding-top:16px;border-top:1px solid #e7e0d3;
       font-size:12.5px;color:#8a8478;line-height:1.75}
  .bar{position:fixed;right:18px;bottom:18px;display:flex;gap:8px}
  .bar button{font:inherit;font-size:13px;padding:9px 14px;border-radius:8px;
    border:1px solid #d9cfb8;background:#fff;color:#3d3a34;cursor:pointer;
    box-shadow:0 2px 8px rgba(0,0,0,.06)}

  /* 手机 */
  @media (max-width:640px){
    body{padding:22px 14px 84px;font-size:15px}
    h1{font-size:22px}
    .card{padding:16px 14px 14px}
    .head h3{font-size:17px}
    .vo p{font-size:16.5px;line-height:1.9}
    .hot-line{padding-left:0;margin-bottom:12px}
  }

  /* 打印 */
  @page{size:A4;margin:12mm 11mm}
  @media print{
    body{padding:0;font-size:10pt;line-height:1.7}
    .wrap{max-width:none}
    .bar,.copy{display:none}
    .kicker{font-size:8pt;margin-bottom:2mm}
    h1{font-size:17pt;margin-bottom:3mm}
    .meta{margin-bottom:3mm}
    .lede{font-size:9pt;margin-bottom:5mm}
    h2{font-size:9.5pt;margin:5mm 0 2.5mm;break-after:avoid}
    .hots li{padding:1.5mm 0 1.5mm 6mm;font-size:10pt}
    .card{break-inside:avoid;page-break-inside:avoid;background:#fff;
          border-color:#d8d2c4;margin-bottom:5mm;padding:5mm 5mm 4mm}
    .num{font-size:16pt}
    .head h3{font-size:13pt}
    .hot-line{font-size:9pt;margin-bottom:2.5mm}
    .vo{padding:3mm 4mm 2mm}
    .vo-bar{margin-bottom:1.5mm}
    .vo p{font-size:10.5pt;line-height:1.7;margin-bottom:2.5mm}
    .shots{margin-top:2.5mm}
    .shots li{font-size:9.5pt;margin-bottom:1mm}
    .foot{margin-top:2.5mm;padding-top:2mm;font-size:8.5pt}
    .cta{font-size:9.5pt;margin-top:2mm}
    .end{margin-top:6mm;padding-top:3mm;font-size:8.5pt}
    a{color:inherit;text-decoration:none}
  }
</style>
</head>
<body>
<div class="wrap">

  <p class="kicker">小狄氧舱 · 自媒体脚本</p>
  <h1>{{城市}} · {{型号简称}} · 本周 10 条</h1>
  <div class="meta">
    <span class="pill">{{型号全称}}</span>
    <span class="pill">{{YYYY-MM-DD}}</span>
    <span class="pill hot">热点：{{实时检索／本周快照／季节常青}}</span>
  </div>
  <p class="lede">{{一句话热点说明：截至哪天、挂上几条、其余为常青选题}}</p>

  <h2>本周能用的热点</h2>
  <ol class="hots">
    <li data-i="01">{{热点标题}}<span class="src">{{来源}} · {{日期}} · 挂到第 {{N}} 条</span></li>
  </ol>

  <h2>十条脚本</h2>

  <article class="card">
    <div class="head">
      <span class="num">01</span>
      <h3>{{标题，12 字以内}}</h3>
      <span class="type">{{算账／避坑／体验／信任／热点}}</span>
    </div>
    <p class="hot-line">挂点：{{哪条热点 → 一句话怎么搭到氧舱上}}</p>

    <div class="vo">
      <div class="vo-bar"><span>{{22}} 秒 · {{105}} 字 · 3 段</span>
        <button class="copy" type="button">复制口播</button></div>
      <p>{{第一段：钩子，前 3 秒说结论}}</p>
      <p>{{第二段}}</p>
      <p>{{第三段：收束}}</p>
    </div>

    <ul class="shots">
      <li>{{你站在舱边说第一句（近景）}}</li>
      <li>{{摇镜扫过空场地（全景）}}</li>
      <li>{{舱门打开、控制屏亮起（特写）}}</li>
    </ul>

    <div class="foot"><span>拍摄 {{15}} 分钟</span><span>难度 ★</span><span>一次可拍 {{3}} 条</span></div>
    <p class="cta"><b>CTA</b>　{{你店里最闲的是哪几个小时？打在评论区。}}</p>
  </article>

  <!-- 02 … 10 同构 -->

  <div class="end">
    <p><b>拍摄顺序</b>　先拍 {{01／04／07}}，同一个位置一次录完，约 {{40}} 分钟；其余可换天。</p>
    <p><b>合规</b>　本批稿件不含功效宣称，不替代医疗建议。经营数字为示例测算，实际以本地客流为准。</p>
    <p>要哪条出完整分镜版，回一句「展开第 N 条」。</p>
  </div>

</div>

<div class="bar"><button type="button" onclick="window.print()">打印 / 存 PDF</button></div>

<script>
document.querySelectorAll('.copy').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var box = btn.closest('.vo');
    var text = Array.prototype.map.call(box.querySelectorAll('p'), function (p) {
      return p.textContent.trim();
    }).filter(Boolean).join('\n\n');
    var done = function () {
      var old = btn.textContent;
      btn.textContent = '已复制';
      setTimeout(function () { btn.textContent = old; }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) {}
      document.body.removeChild(ta);
    }
  });
});
</script>
</body>
</html>
```

---

## 四、组件怎么写

### 编号
两位数字，`01`–`10`，等宽字体，暖金。**不要用圆圈数字或 emoji**——打印会缺字。

### 类型徽标
只用五个词：算账、避坑、体验、信任、热点。**不要写「干货」「必看」「爆款」**，那是 C 端话术，B 端老板看了会关掉。

### 口播区
三个 `<p>`，一段一个镜头。**段间不空行**（CSS 已经有 margin），空行会让经销商以为要停。
时长与字数写在 `.vo-bar` 里，跟实际字数必须对得上——这条是硬要求，字数错了整份的可信度就没了。

### 镜头
写「你店里怎么拍」：`舱门打开、控制屏亮起（特写）`。
不写 `B-roll`、`空镜`、`转场`。他不会剪，写了他也只拍第一个。

### 元信息条
拍摄耗时／难度／一次能拍几条。三样都要，缺了「一次能拍几条」他就以为十条要拍一天。

### 页脚
必须有合规声明那一行。这是经销商拿去发之前最后看到的东西。

---

## 五、完整分镜版怎么放

展开单条时不要另开一个文件，用**同一个文件追加**或在顶部插一张「重点卡」+ 折叠区分镜表。

分镜表在手机上会挤爆，处理办法：

```css
.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px 0}
table{width:100%;min-width:620px;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #ece5d8;vertical-align:top}
th{font-size:12px;color:#8a8478;font-weight:600;white-space:nowrap}
```

外层套 `.table-wrap` 就能横向滑动，不会把整页撑破。

---

## 六、写完自检（四项，30 秒）

1. 双击打开，顶部三秒内能看出「哪个城市、什么型号、哪天的热点」——看不出就是顶栏没做对
2. 拉到手机宽度（DevTools 或直接手机开），口播字号还够大、卡片不横向溢出
3. `Ctrl+P` 预览：卡片没被切断、页脚合规声明还在
4. 点一次「复制口播」，粘到记事本里，三段都在、没串行

---

## 七、常见错误

| 错误 | 后果 | 改法 |
|---|---|---|
| 引了 Google Fonts / 图标 CDN | 店里断网变方块，整页乱 | 只用系统字体，图标用文字或 CSS 画 |
| 直接把 Markdown 塞进 `<pre>` | 看起来像代码，经销商以为是给他程序员看的 | 一字段一组件，用真 HTML |
| 卡片用深色底 + 白字 | 打印出来一坨黑，费墨 | 白底或极浅暖底，深色字 |
| 十条全塞一页不分隔 | 找不到第几条 | 一卡一条，卡间距 18px |
| 用 emoji 当编号 | 打印缺字、不同手机显示不一样 | 两位数字，等宽字体 |
| 口播标 22 秒实际 130 字 | 拍出来超时，多录一遍就烦了 | 写完数字数，4.7 字/秒 |
