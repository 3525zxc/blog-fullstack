"""种子数据：首次启动自动写入演示内容（与前端原演示数据一致）。"""
from .extensions import db
from .models import (Category, Sub, Post, Comment, Guest, Setting, Admin)

CATS = [
    {'id': 'tech', 'name': '技术', 'icon': 'code', 'desc': '代码、架构与工具，工程师的修炼场', 'sort': 0, 'subs': [
        {'id': 'frontend', 'name': '前端开发', 'desc': 'HTML / CSS / JavaScript'},
        {'id': 'backend', 'name': '后端架构', 'desc': '服务端、数据与部署'},
        {'id': 'ai', 'name': '人工智能', 'desc': '模型、工具与思考'}]},
    {'id': 'life', 'name': '生活', 'icon': 'coffee', 'desc': '工作之外，还有一整个世界', 'sort': 1, 'subs': [
        {'id': 'essay', 'name': '随笔手记', 'desc': '深夜与清晨的碎念'},
        {'id': 'travel', 'name': '旅行足迹', 'desc': '去过的地方与遇见的人'},
        {'id': 'food', 'name': '美食日常', 'desc': '一个人也要好好吃饭'}]},
    {'id': 'design', 'name': '设计', 'icon': 'sun', 'desc': '美感是一种纪律', 'sort': 2, 'subs': [
        {'id': 'ui', 'name': 'UI 设计', 'desc': '界面、交互与体验'},
        {'id': 'photo', 'name': '摄影美学', 'desc': '光影与构图'},
        {'id': 'inspire', 'name': '灵感收藏', 'desc': '值得反复看的东西'}]},
]

POSTS = [
    {
        'id': 'p1', 'title': 'CSS Grid 布局完全指南：从入门到实战', 'cat': 'frontend',
        'tags': ['CSS', '布局', '前端'], 'cover': 0, 'status': 'published', 'date': '2026-10-18',
        'views': 1326, 'likes': 42, 'excerpt': 'Flexbox 管“流”，Grid 管“格”。一篇笔记搞懂二维布局的核心心智模型与三个常见坑。',
        'content':
'<h2>为什么是 Grid，而不是 Flexbox？</h2>'
'<p>Flexbox 是一维布局的王者：一行或一列，元素沿着主轴流动，非常适合导航栏、工具栏、按钮组这类场景。但当你需要同时控制行和列——比如一个真正响应式的卡片墙——Flexbox 就需要大量嵌套和计算才能勉强胜任。</p>'
'<p>Grid 的出现把“二维布局”变成了浏览器的一等公民。你只需要在容器上声明网格，然后告诉每个元素占哪几行哪列，剩下的交给浏览器。</p>'
'<blockquote>一句话总结：Flexbox 管“流”，Grid 管“格”。两者不是替代关系，而是搭档。</blockquote>'
'<h2>一分钟上手</h2>'
'<p>把一个容器变成网格只需要一行 CSS：</p>'
'<pre><code>.wall {\n  display: grid;\n  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));\n  gap: 20px;\n}</code></pre>'
'<p>这一行代码的意思是：列数自动计算，每列至少 240px，剩余空间平均分配。无需任何媒体查询，卡片墙就能从 1 列平滑过渡到 4 列。</p>'
'<h2>实战：可响应的文章卡片墙</h2>'
'<p>本站首页的文章墙正是用上面的模式实现的。更进一步，我们让第一张卡片跨两列，形成视觉锚点：</p>'
'<pre><code>.post-card:first-child {\n  grid-column: span 2;\n}\n@media (max-width: 720px) {\n  .post-card:first-child { grid-column: span 1; }\n}</code></pre>'
'<h2>三个容易踩的坑</h2>'
'<ul>'
'<li><strong>隐式行高塌陷</strong>：内容比预期高时，用 <code>grid-auto-rows: minmax(180px, auto)</code> 保底。</li>'
'<li><strong>间距叠加</strong>：<code>gap</code> 同时作用于行与列，不要再给子元素加 margin。</li>'
'<li><strong>命名线难维护</strong>：简单场景用 <code>span</code>，复杂场景再用 <code>grid-template-areas</code>。</li>'
'</ul>'
'<p>Grid 的学习曲线比 Flexbox 陡，但回报也更高。花一个下午读完 MDN 的教程，你会回来感谢自己。</p>'
    },
    {
        'id': 'p2', 'title': '不用框架，用原生 JS 写一个富文本编辑器', 'cat': 'frontend',
        'tags': ['JavaScript', '项目', '前端'], 'cover': 2, 'status': 'published', 'date': '2026-10-12',
        'views': 986, 'likes': 31, 'excerpt': 'contenteditable + document.execCommand，两百行代码实现一个能用的编辑器，顺便搞清楚浏览器到底在做什么。',
        'content':
'<h2>核心其实只有一个属性</h2>'
'<p>让一个 div 变成可编辑区域，只需要 <code>contenteditable="true"</code>。浏览器会自动处理光标、输入、选区，甚至粘贴。我们要做的，只是把用户的意图（点击“加粗”）翻译成浏览器能懂的指令。</p>'
'<h2>用 execCommand 执行格式命令</h2>'
'<pre><code>function exec(cmd, value) {\n  document.execCommand(cmd, false, value || null);\n  editor.focus();\n}\n\nboldBtn.addEventListener("click", () => exec("bold"));</code></pre>'
'<p>虽然 execCommand 已被标记为废弃，但浏览器短期内不会移除它，而且它是唯一能在保持光标位置的同时修改富文本的原生 API。</p>'
'<h2>划词工具栏</h2>'
'<p>监听 <code>mouseup</code>，用 <code>window.getSelection()</code> 判断是否有选中文本，然后根据 <code>range.getBoundingClientRect()</code> 把工具栏定位到选区上方。细节在于：点击工具栏本身不能让选区消失，所以工具栏的 mousedown 要 <code>preventDefault()</code>。</p>'
'<h2>踩坑记录</h2>'
'<ul>'
'<li>粘贴 Word 内容会带入一堆垃圾标签，需要在 paste 事件里只取 <code>text/plain</code>。</li>'
'<li>输入法的 composition 事件要和 input 事件区分开，否则中文统计会抖。</li>'
'<li>撤销栈是浏览器管的，手动改 DOM 后 Ctrl+Z 的表现会和你想的不一样。</li>'
'</ul>'
'<p>结论：自研编辑器适合“够用就好”的场景。如果要做协同编辑，还是得上 ProseMirror 这类专业方案。</p>'
    },
    {
        'id': 'p3', 'title': 'RESTful API 设计的 10 个最佳实践', 'cat': 'backend',
        'tags': ['API', '架构', '后端'], 'cover': 5, 'status': 'published', 'date': '2026-10-06',
        'views': 742, 'likes': 19, 'excerpt': 'URL 用名词不用动词、状态码用对、错误信息带 traceId——一份可以直接贴在工位上的清单。',
        'content':
'<h2>资源与命名</h2>'
'<ul>'
'<li>URL 表示资源，用名词复数：<code>/articles</code>，不要 <code>/getArticles</code>。</li>'
'<li>用 HTTP 方法表达动作：GET 查、POST 增、PUT 改、DELETE 删。</li>'
'<li>层级不超过两层，再深就用查询参数：<code>/articles/12/comments</code> 可以，<code>/a/1/b/2/c/3</code> 不行。</li>'
'</ul>'
'<h2>状态码与错误体</h2>'
'<p>200 不是万能药。创建成功返回 201，删除成功返回 204，参数错误返回 400，未授权 401，无权限 403，找不到 404，冲突 409。错误响应统一带一个机器可读的 code 和一个给人看的 message：</p>'
'<pre><code>{\n  "code": "ARTICLE_NOT_FOUND",\n  "message": "文章不存在或已删除",\n  "traceId": "a1b2c3d4"\n}</code></pre>'
'<h2>分页、过滤与版本</h2>'
'<ul>'
'<li>列表一律分页，用 <code>?page=1&amp;size=20</code>，并返回总数。</li>'
'<li>过滤、排序、字段选择都用查询参数，不要发明新端点。</li>'
'<li>大版本进路径（<code>/v1/articles</code>），小版本靠新增字段平滑演进。</li>'
'</ul>'
'<blockquote>好的 API 是“可预测”的：看 URL 就知道会发生什么，看状态码就知道结果如何。</blockquote>'
    },
    {
        'id': 'p4', 'title': '我把 AI 当作结对编程伙伴的一周', 'cat': 'ai',
        'tags': ['AI', '效率', '思考'], 'cover': 3, 'status': 'published', 'date': '2026-09-28',
        'views': 1580, 'likes': 56, 'excerpt': '从怀疑到默契，再到重新划清边界——记录一次真实的人机协作实验，以及我最后保留的三条使用原则。',
        'content':
'<h2>第一天：将信将疑</h2>'
'<p>我给自己定了一条规矩：AI 生成的每一行代码，都必须读懂后才能提交。第一天下来，进度反而慢了——但奇怪的是，Bug 数少了。</p>'
'<h2>第三天：找到默契</h2>'
'<p>秘诀是把问题问对。不要说“帮我写个函数”，而是说“这个函数输入是 A，输出是 B，边界情况有 C，我现在的写法在 D 场景会错，帮我看下逻辑”。上下文越具体，建议越可用。</p>'
'<h2>第五天：边界浮现</h2>'
'<p>AI 在我熟悉的领域是加速器，在陌生的领域是“自信的陷阱”——它能流畅地编造不存在的 API。那一周我踩了两次，都是它非常肯定、而实际不存在的方法。</p>'
'<h2>我最终保留的三条原则</h2>'
'<ol>'
'<li>AI 负责草稿与枚举，我负责判断与取舍。</li>'
'<li>凡是涉及钱、权限、删除的操作，人工二次确认。</li>'
'<li>每天留 30 分钟不借助 AI 纯手写，保持手感。</li>'
'</ol>'
'<blockquote>工具不会取代程序员，但“会用工具的程序员”会取代不用的。</blockquote>'
    },
    {
        'id': 'p5', 'title': '深夜咖啡馆里的编程随想', 'cat': 'essay',
        'tags': ['随笔', '深夜', '生活'], 'cover': 4, 'status': 'published', 'date': '2026-09-21',
        'views': 623, 'likes': 27, 'excerpt': '十一点半的咖啡馆，键盘声和咖啡机蒸汽声混在一起。有些 bug 白天修不好，晚上却自己投降了。',
        'content':
'<h2>属于夜晚的带宽</h2>'
'<p>白天的时间是被切碎的：消息、会议、突然的需求。只有深夜留出一段完整的带宽，容得下一个难题从“看不懂”到“原来如此”的全过程。</p>'
'<h2>咖啡馆是人类缓冲区</h2>'
'<p>在家办公第三年，我发现人需要“第三空间”。咖啡馆恰好是一种人类缓冲区：周围有人声，但没人跟你说话；有背景噪音，但盖不住思路流动的声音。</p>'
'<blockquote>写代码是和机器对话，而深夜咖啡馆提醒你：你首先是一个人类。</blockquote>'
'<h2>一个奇怪的发现</h2>'
'<p>很多白天调试不出来的问题，晚上十一点后会“自己投降”。后来才明白，不是夜晚有魔法，而是白天被无数上下文切换磨掉的耐心，在夜里重新长回来了。</p>'
'<p>如果你也正为一个 bug 焦头烂额，不妨先关掉电脑，去楼下走一圈。答案经常在松开拳头之后出现。</p>'
    },
    {
        'id': 'p6', 'title': '京都七日：古寺、红叶与抹茶', 'cat': 'travel',
        'tags': ['旅行', '日本', '摄影'], 'cover': 6, 'status': 'published', 'date': '2026-09-14',
        'views': 1104, 'likes': 48, 'excerpt': '一篇迟到的旅行记：清水寺的清晨、岚山竹林的回声、鸭川边的落日，以及那些比景点更动人的日常。',
        'content':
'<h2>行程概览</h2>'
'<ul>'
'<li>D1-D2 东山：清水寺、二年坂、八坂神社的夜</li>'
'<li>D3-D4 岚山：竹林、渡月桥、祐斋亭的窗</li>'
'<li>D5-D6 洛北：贵船神社、琉璃光院</li>'
'<li>D7 鸭川：什么都不做的一天</li>'
'</ul>'
'<h2>清水寺的清晨</h2>'
'<p>六点前到，舞台上只有打扫的僧人和几只乌鸦。阳光从东山翻过来的时候，整座木殿是金色的。旅行教会我最重要的事之一：景点在开门前和关门后，是两个世界。</p>'
'<h2>比景点更动人的</h2>'
'<p>是清晨面包店刚出炉的菠萝油气味，是公交上给老人让座的中学生，是鸭川边练习滑板的少年。景点是明信片，日常才是目的地。</p>'
'<blockquote>下次想去大阪，不为环球影城，只为深夜小巷里那碗热腾腾的关东煮。</blockquote>'
    },
    {
        'id': 'p7', 'title': '2026 年 UI 设计趋势观察笔记', 'cat': 'ui',
        'tags': ['设计', 'UI', '趋势'], 'cover': 8, 'status': 'published', 'date': '2026-09-08',
        'views': 878, 'likes': 35, 'excerpt': '大字号回归、玻璃拟态退潮、暗色默认化——以及一个老生常谈但愈发重要的命题：可访问性不是功能，是底线。',
        'content':
'<h2>趋势一：大字号与强对比回来了</h2>'
'<p>移动端优先的这些年，正文 14px 曾是默认值。而在折叠屏与车机屏普及后，大家发现：可读性永远比“信息密度”重要。H1 用 40px+ 正在成为新常态。</p>'
'<h2>趋势二：玻璃拟态退潮</h2>'
'<p>毛玻璃用了三年，用户开始疲劳——它让层级变模糊，也让对比度难达标。2026 年的方向是“半透明 + 明确描边”，既保留通透感，又不牺牲清晰度。</p>'
'<h2>趋势三：暗色从“附加题”变“默认项”</h2>'
'<p>越来越多的产品在首次启动时询问主题偏好，而不是把暗色藏在设置里三级菜单。设计令牌（Design Token）让这件事的成本降到了历史最低。</p>'
'<h2>不变的命题</h2>'
'<p>趋势每年翻新，但有一条越来越清晰：可访问性不是附加功能，而是底线。对比度 4.5:1、焦点可见、尊重 reduce-motion——这些不是“加分项”，是“及格线”。</p>'
    },
    {
        'id': 'p8', 'title': '手机摄影入门：把日常拍成电影', 'cat': 'photo',
        'tags': ['摄影', '手机', '构图'], 'cover': 9, 'status': 'published', 'date': '2026-09-02',
        'views': 655, 'likes': 22, 'excerpt': '不需要买单反，先用好手里的手机：三分法之外的四种构图、一天中最好的两小时光、以及克制使用滤镜。',
        'content':
'<h2>构图：先打破三分法</h2>'
'<p>三分法是好的起点，但不是终点。试试：引导线（道路、栏杆）、框架构图（门窗）、对称与重复（地铁站、菜市场）、以及留白——给画面留一口气。</p>'
'<h2>光线：一天中的两小时</h2>'
'<p>日出后一小时和日落前一小时，光是有颜色和方向的。正午的顶光最单调，尽量安排在室内或拍剪影。阴天其实是天然的巨大柔光箱，拍人像特别好。</p>'
'<h2>后期：克制是最高级的滤镜</h2>'
'<ul>'
'<li>先裁图，再调色——构图能救一半的照片。</li>'
'<li>对比度 +10、阴影 +15，是万能的“通透”起点。</li>'
'<li>滤镜浓度不超过 30%，否则细节会死。</li>'
'</ul>'
'<blockquote>最好的相机，是你愿意随身带出去的那一台。</blockquote>'
    },
]

COMMENTS = [
    {'id': 'c1', 'postId': 'p1', 'parent': None, 'name': '阿澈', 'color': 1, 'content': 'auto-fill + minmax 这个写法太优雅了，马上用到我的项目里！', 'date': '2026-10-19', 'status': 'approved', 'likes': 5},
    {'id': 'c2', 'postId': 'p1', 'parent': 'c1', 'name': '大谢', 'color': 0, 'content': '谢谢支持！下一篇写 Grid 命名线的进阶用法，欢迎回来看看。', 'date': '2026-10-19', 'status': 'approved', 'likes': 2},
    {'id': 'c3', 'postId': 'p1', 'parent': None, 'name': 'Bug 猎人', 'color': 2, 'content': '第一张卡片跨两列在窄屏没做处理，建议补个断点。', 'date': '2026-10-20', 'status': 'pending', 'likes': 0},
    {'id': 'c4', 'postId': 'p2', 'parent': None, 'name': '尤加利', 'color': 3, 'content': 'execCommand 虽然废弃但确实香，文章里提到的 composition 坑我上周刚踩到。', 'date': '2026-10-13', 'status': 'approved', 'likes': 3},
    {'id': 'c5', 'postId': 'p2', 'parent': None, 'name': '深夜coder', 'color': 4, 'content': '请问划词工具栏的定位代码会开源吗？很想学。', 'date': '2026-10-15', 'status': 'approved', 'likes': 1},
    {'id': 'c6', 'postId': 'p3', 'parent': None, 'name': '后端老张', 'color': 5, 'content': 'traceId 这条真的太重要了，排查问题能少扯一半的皮。', 'date': '2026-10-07', 'status': 'approved', 'likes': 4},
    {'id': 'c7', 'postId': 'p4', 'parent': None, 'name': '半糖', 'color': 6, 'content': '“AI 在陌生领域是自信的陷阱”，这句话我要抄进笔记本。', 'date': '2026-09-29', 'status': 'approved', 'likes': 6},
    {'id': 'c8', 'postId': 'p5', 'parent': None, 'name': '拿铁不加糖', 'color': 7, 'content': '深夜咖啡馆 +1，我家楼下那家凌晨一点还开着。', 'date': '2026-09-22', 'status': 'approved', 'likes': 2},
    {'id': 'c9', 'postId': 'p5', 'parent': None, 'name': '路过的风', 'color': 8, 'content': '“答案经常在松开拳头之后出现”，治愈了今晚改 bug 的我。', 'date': '2026-09-23', 'status': 'approved', 'likes': 3},
    {'id': 'c10', 'postId': 'p6', 'parent': None, 'name': '红叶收藏家', 'color': 9, 'content': '祐斋亭的窗！那扇窗里的四季是我见过最美的取景框。', 'date': '2026-09-16', 'status': 'approved', 'likes': 4},
    {'id': 'c11', 'postId': 'p8', 'parent': None, 'name': '扫街小王子', 'color': 0, 'content': '正午顶光拍剪影这个技巧试过，出片率意外地高。', 'date': '2026-09-05', 'status': 'pending', 'likes': 1},
]

GUESTS = [
    {'id': 'g1', 'name': '路过的小白', 'color': 2, 'content': '博客风格好干净，请问是手写的主题吗？想求一个模板。', 'date': '2026-10-17', 'likes': 6},
    {'id': 'g2', 'name': '前端萌新', 'color': 4, 'content': '从 Grid 那篇跟过来的，干货满满，已三连！', 'date': '2026-10-16', 'likes': 3},
    {'id': 'g3', 'name': '产品汪', 'color': 6, 'content': '作为产品也被那篇 AI 协作周记戳中了，期待更多跨界思考。', 'date': '2026-10-11', 'likes': 5},
    {'id': 'g4', 'name': '夜猫子', 'color': 8, 'content': '留言板这个功能好，占了块地皮，以后常来。', 'date': '2026-10-09', 'likes': 2},
    {'id': 'g5', 'name': '摄影师阿May', 'color': 1, 'content': '手机摄影那篇受教了，原来我缺的不是设备是构图。', 'date': '2026-10-03', 'likes': 4},
]

SETTINGS = {
    'siteName': '林间漫记',
    'sub': '记录代码、设计与生活的交汇点',
    'author': '大谢',
    'sign': '前端工程师 / 业余摄影爱好者',
    'intro': '你好，我是大谢。白天写前端，晚上写文字，周末按快门。这里是我的数字自留地，记录技术笔记、设计观察与生活切片。',
    'accent': '#5b5bd6',
    'startedAt': '2024-03-01',
}

# 默认管理员：admin / admin123 （部署后请立刻修改）
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


def seed_all():
    """写入演示数据（在 app 上下文中调用）。"""
    for c in CATS:
        db.session.add(Category(id=c['id'], name=c['name'], icon=c['icon'],
                                desc=c['desc'], sort=c['sort']))
    db.session.flush()
    for c in CATS:
        for s in c['subs']:
            db.session.add(Sub(id=s['id'], name=s['name'], desc=s['desc'], cat_id=c['id']))

    for p in POSTS:
        db.session.add(Post(
            id=p['id'], title=p['title'], excerpt=p['excerpt'], content=p['content'],
            cat=p['cat'], tags=p['tags'], cover=p['cover'], status=p['status'],
            date=p['date'], views=p['views'], likes=p['likes'], local=False))

    for c in COMMENTS:
        db.session.add(Comment(
            id=c['id'], post_id=c['postId'], parent=c['parent'], name=c['name'],
            color=c['color'], content=c['content'], date=c['date'],
            status=c['status'], likes=c['likes']))

    for g in GUESTS:
        db.session.add(Guest(id=g['id'], name=g['name'], color=g['color'],
                             content=g['content'], date=g['date'], likes=g['likes']))

    for k, v in SETTINGS.items():
        db.session.add(Setting(key=k, value=v))

    admin = Admin(username=ADMIN_USERNAME)
    admin.set_password(ADMIN_PASSWORD)
    db.session.add(admin)

    db.session.commit()


if __name__ == '__main__':
    # 也可独立运行：python -m server.seed
    from .app import create_app
    app = create_app()
    with app.app_context():
        seed_all()
    print('种子数据写入完成')
