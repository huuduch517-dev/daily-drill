# -*- coding: utf-8 -*-
"""由 index.html 生成本地单文件版（双击即用，不依赖服务器和网络）。
改了 index.html 之后重跑一次即可，两边不会走散。"""
import io, os, re, sys, base64

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'index.html'), encoding='utf-8').read()
h = src

# 1) manifest 和 sw 在 file:// 下没有意义，去掉免得报错
h = re.sub(r'\s*<link rel="manifest"[^>]*>', '', h)
h = re.sub(r"\s*if\('serviceWorker'in navigator&&location\.protocol\.startsWith\('http'\)\)\s*\n"
           r"\s*navigator\.serviceWorker\.register\('sw\.js'\)\.catch\(\(\)=>\{\}\);", '', h)

# 2) 图标内联成 data URI，单文件才真的是单文件
ico = os.path.join(here, 'icon-180.png')
if os.path.exists(ico):
    b64 = base64.b64encode(open(ico, 'rb').read()).decode()
    h = re.sub(r'<link rel="apple-touch-icon" href="[^"]*">',
               '<link rel="apple-touch-icon" href="data:image/png;base64,%s">' % b64, h)
    h = h.replace('<link rel="apple-touch-icon"',
                  '<link rel="icon" href="data:image/png;base64,%s">\n<link rel="apple-touch-icon"' % b64, 1)

# 3) 标题上标一下，跟线上版区分开
h = h.replace('<title>日课 · 站桩 + 八部金刚功</title>',
              '<title>日课 · 站桩 + 八部金刚功（本地版）</title>')

out = os.path.join(here, '日课-本地版.html')
open(out, 'w', encoding='utf-8').write(h)

assert '<link rel="manifest"' not in h, 'manifest 未清除'
assert 'serviceWorker.register' not in h, 'sw 注册未清除'
assert h.rstrip().endswith('</html>'), '文件结尾不完整'
# 换视频时记得同步这份清单，否则这里会拦下来（这是有意的）
for bv, why in (('BV1YT421y76x', '站桩'), ('BV1aM411z7bS', '金刚功'), ('BV1wtoUBmE6N', '工作间歇抗阻')):
    assert bv in h, '缺少%s视频 %s' % (why, bv)
assert 'brInit' in h and 'musicStart' in h, '4-7-8 呼吸模块缺失'
print('已生成: %s  (%.1f KB)' % (out, len(h.encode('utf-8')) / 1024))
print('校验通过：无 manifest / 无 sw 注册 / 视频齐全 / 呼吸模块在 / 结尾完整')
