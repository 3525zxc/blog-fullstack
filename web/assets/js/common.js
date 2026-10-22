/* =========================================================
 * common.js — 共享交互层
 * 导航 / 主题 / Toast / 模态框 / 组件渲染 / Markdown 迷你渲染器
 * ========================================================= */
window.Blog = (function () {
  'use strict';
  var D = window.BlogData;

  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function getParam(name) {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
  }

  /* ---------------- 图标（内联 SVG，无图片） ---------------- */
  var ICONS = {
    home: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    code: '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    coffee: '<path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    archive: '<polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5" rx="1"/><line x1="10" y1="12" x2="14" y2="12"/>',
    user: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    users: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    search: '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    moon: '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
    heart: '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l8.84 8.84 8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/>',
    star: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26"/>',
    share: '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/>',
    message: '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    eye: '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    edit: '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>',
    trash: '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    check: '<polyline points="20 6 9 17 4 12"/>',
    plus: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    chart: '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    sliders: '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
    menu: '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>',
    x: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    arrow: '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    clock: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    tag: '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
    calendar: '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    send: '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
    reply: '<polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 0 0-4-4H4"/>',
    refresh: '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
    github: '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22 6 12 13 2 6"/>',
    rss: '<path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>',
    compass: '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    sparkles: '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9L19 15z"/>',
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    globe: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
  };
  function icon(name, cls) {
    return '<svg class="icon ' + (cls || '') + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (ICONS[name] || '') + '</svg>';
  }

  /* ---------------- 主题 ---------------- */
  var THEME_KEY = 'linblog_theme';
  function getTheme() {
    try { return localStorage.getItem(THEME_KEY) || 'light'; } catch (e) { return 'light'; }
  }
  function setTheme(t) {
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
    document.documentElement.setAttribute('data-theme', t);
    $$('[data-theme-btn]').forEach(function (b) {
      b.innerHTML = icon(t === 'dark' ? 'sun' : 'moon');
      b.title = t === 'dark' ? '切换为浅色模式' : '切换为深色模式';
    });
  }
  function toggleTheme() { setTheme(getTheme() === 'dark' ? 'light' : 'dark'); }

  /* ---------------- 主色调 ---------------- */
  function applyAccent() {
    var accent = D.getSettings().accent || '#5b5bd6';
    var r = parseInt(accent.slice(1, 3), 16), g = parseInt(accent.slice(3, 5), 16), b = parseInt(accent.slice(5, 7), 16);
    document.documentElement.style.setProperty('--primary', accent);
    document.documentElement.style.setProperty('--primary-soft', 'rgba(' + r + ',' + g + ',' + b + ',0.12)');
    document.documentElement.style.setProperty('--primary-border', 'rgba(' + r + ',' + g + ',' + b + ',0.35)');
  }

  /* ---------------- 顶部导航 ---------------- */
  function navItems() {
    var items = [{ key: 'index', label: '首页', href: 'index.html', icon: 'home' }];
    D.getCats().forEach(function (c) {
      items.push({
        key: c.id, label: c.name, icon: c.icon, href: 'category.html?main=' + c.id,
        children: c.subs.map(function (s) {
          return { key: s.id, label: s.name, href: 'category.html?cat=' + s.id, desc: s.desc };
        })
      });
    });
    items.push({
      key: 'archive', label: '归档', icon: 'archive', href: 'archive.html',
      children: [
        { key: 'timeline', label: '时间线', href: 'archive.html?tab=timeline', desc: '按年月浏览全部文章' },
        { key: 'tags', label: '标签云', href: 'archive.html?tab=tags', desc: '发现内容之间的关联' },
        { key: 'cats', label: '分类总览', href: 'archive.html?tab=cats', desc: '一图看完全部分类' }
      ]
    });
    items.push({
      key: 'about', label: '关于', icon: 'user', href: 'about.html',
      children: [
        { key: 'about', label: '关于我', href: 'about.html', desc: '我是谁，我在做什么' },
        { key: 'guestbook', label: '留言板', href: 'guestbook.html', desc: '留下你的足迹' },
        { key: 'resume', label: '我的履历', href: 'about.html#resume', desc: '一路走过的时间节点' }
      ]
    });
    return items;
  }

  function renderHeader(active) {
    var root = document.getElementById('header-root');
    if (!root) return;
    var s = D.getSettings();
    var navHtml = navItems().map(function (item) {
      var isActive = item.key === active;
      var childActive = item.children && item.children.some(function (c) { return c.key === active; });
      if (isActive || childActive) isActive = true;
      var html = '<div class="nav-item' + (item.children ? ' has-drop' : '') + (isActive ? ' active' : '') + '">';
      html += '<a class="nav-link" href="' + item.href + '">' + icon(item.icon) + '<span>' + item.label + '</span>';
      if (item.children) html += icon('arrow', 'chev');
      html += '</a>';
      if (item.children) {
        html += '<div class="dropdown"><div class="dropdown-title">' + item.label + '专栏</div>' +
          item.children.map(function (c) {
            return '<a class="drop-link' + (c.key === active ? ' active' : '') + '" href="' + c.href + '">' +
              '<span class="drop-name">' + c.label + '</span>' +
              (c.desc ? '<span class="drop-desc">' + c.desc + '</span>' : '') + '</a>';
          }).join('') + '</div>';
      }
      html += '</div>';
      return html;
    }).join('');

    root.innerHTML =
      '<header class="site-header" id="siteHeader">' +
        '<div class="container header-inner">' +
          '<a class="logo" href="index.html">' +
            '<span class="logo-mark">' + esc(s.siteName.charAt(0)) + '</span>' +
            '<span class="logo-text">' + esc(s.siteName) + '<small>' + esc(s.sub) + '</small></span>' +
          '</a>' +
          '<nav class="main-nav" id="mainNav">' + navHtml +
            '<a class="nav-link admin-entry" href="admin/login.html">' + icon('sliders') + '<span>管理后台</span></a>' +
          '</nav>' +
          '<div class="header-actions">' +
            '<form class="search-box" id="headerSearch" action="search.html" method="get">' +
              icon('search') +
              '<input type="text" name="q" placeholder="搜索文章…" autocomplete="off">' +
            '</form>' +
            '<button class="icon-btn" data-theme-btn title="切换主题"></button>' +
            '<button class="icon-btn nav-toggle" id="navToggle" title="菜单">' + icon('menu') + '</button>' +
          '</div>' +
        '</div>' +
      '</header>';

    setTheme(getTheme());
    wireHeader();
  }

  function wireHeader() {
    /* 主题按钮 */
    $$('[data-theme-btn]').forEach(function (b) {
      b.addEventListener('click', toggleTheme);
    });
    /* 移动端菜单 */
    var toggle = $('#navToggle');
    var nav = $('#mainNav');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = document.body.classList.toggle('nav-open');
        nav.classList.toggle('open', open);
        toggle.innerHTML = icon(open ? 'x' : 'menu');
      });
    }
    /* 下拉菜单：点击切换（触屏），点击空白关闭 */
    $$('.nav-item.has-drop > .nav-link').forEach(function (link) {
      link.addEventListener('click', function (e) {
        if (window.matchMedia('(hover: none)').matches) {
          e.preventDefault();
          var item = link.parentElement;
          var was = item.classList.contains('open');
          $$('.nav-item.has-drop').forEach(function (n) { n.classList.remove('open'); });
          if (!was) item.classList.add('open');
        }
      });
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.nav-item.has-drop')) {
        $$('.nav-item.has-drop').forEach(function (n) { n.classList.remove('open'); });
      }
    });
    /* 移动端：点击导航链接后收起菜单 */
    $$('#mainNav a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        if (nav) nav.classList.remove('open');
        if (toggle) toggle.innerHTML = icon('menu');
      });
    });
  }

  /* ---------------- 页脚 ---------------- */
  function renderFooter() {
    var root = document.getElementById('footer-root');
    if (!root) return;
    var s = D.getSettings();
    var cats = D.getCats();
    var stats = D.getStats();
    root.innerHTML =
      '<footer class="site-footer">' +
        '<div class="container footer-grid">' +
          '<div class="footer-col footer-about">' +
            '<div class="logo footer-logo"><span class="logo-mark">' + esc(s.siteName.charAt(0)) + '</span>' +
            '<span class="logo-text">' + esc(s.siteName) + '</span></div>' +
            '<p>' + esc(s.intro) + '</p>' +
            '<div class="social-row">' +
              '<button class="icon-btn" data-social="GitHub" title="GitHub">' + icon('github') + '</button>' +
              '<button class="icon-btn" data-social="邮箱" title="邮箱">' + icon('mail') + '</button>' +
              '<button class="icon-btn" data-social="RSS" title="RSS 订阅">' + icon('rss') + '</button>' +
              '<button class="icon-btn" data-social="微信" title="微信">' + icon('message') + '</button>' +
            '</div>' +
          '</div>' +
          '<div class="footer-col">' +
            '<h4>快速导航</h4>' +
            '<a href="index.html">首页</a><a href="archive.html?tab=timeline">文章归档</a>' +
            '<a href="archive.html?tab=tags">标签云</a><a href="about.html">关于我</a>' +
            '<a href="guestbook.html">留言板</a><a href="admin/login.html">管理后台</a>' +
          '</div>' +
          '<div class="footer-col">' +
            '<h4>内容分类</h4>' +
            cats.map(function (c) { return '<a href="category.html?main=' + c.id + '">' + esc(c.name) + '</a>'; }).join('') +
          '</div>' +
          '<div class="footer-col">' +
            '<h4>订阅更新</h4>' +
            '<p class="footer-tip">新文章发布时，第一时间送达你的邮箱。</p>' +
            '<form class="subscribe-form" id="subscribeForm">' +
              '<input type="email" placeholder="your@email.com" required>' +
              '<button class="btn btn-primary btn-sm" type="submit">订阅</button>' +
            '</form>' +
            '<div class="footer-stats">' +
              '<span>' + icon('file') + ' ' + stats.published + ' 篇文章</span>' +
              '<span>' + icon('message') + ' ' + stats.comments + ' 条评论</span>' +
              '<span>' + icon('clock') + ' 已运行 ' + stats.days + ' 天</span>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="container footer-bottom">' +
          '<span>© ' + new Date().getFullYear() + ' ' + esc(s.siteName) + ' · ' + esc(s.author) + ' 版权所有</span>' +
          '<span class="footer-note">本站为高保真交互原型 · 数据存储于浏览器本地 · 未接入真实后端</span>' +
        '</div>' +
      '</footer>';

    $$('[data-social]').forEach(function (b) {
      b.addEventListener('click', function () {
        toast('演示原型：' + b.getAttribute('data-social') + ' 链接暂未配置', 'info');
      });
    });
    var form = $('#subscribeForm');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        toast('订阅成功！新文章会第一时间通知你（演示）');
        form.reset();
      });
    }
  }

  /* ---------------- Toast ---------------- */
  function toastRoot() {
    var r = document.getElementById('toastRoot');
    if (!r) {
      r = document.createElement('div');
      r.id = 'toastRoot';
      r.className = 'toast-root';
      document.body.appendChild(r);
    }
    return r;
  }
  function toast(msg, type, action) {
    type = type || 'success';
    var t = document.createElement('div');
    t.className = 'toast toast-' + type;
    t.innerHTML = '<span class="toast-icon">' + icon(type === 'error' ? 'x' : type === 'info' ? 'message' : 'check') + '</span>' +
      '<span class="toast-msg">' + esc(msg) + '</span>' +
      (action ? '<button class="toast-action">' + esc(action.label) + '</button>' : '') +
      '<button class="toast-close" title="关闭">' + icon('x') + '</button>';
    toastRoot().appendChild(t);
    requestAnimationFrame(function () { t.classList.add('show'); });
    var timer = setTimeout(close, 3400);
    function close() {
      clearTimeout(timer);
      t.classList.remove('show');
      setTimeout(function () { t.remove(); }, 300);
    }
    $('.toast-close', t).addEventListener('click', close);
    var act = $('.toast-action', t);
    if (act) act.addEventListener('click', function () { close(); if (action.href) location.href = action.href; });
  }

  /* ---------------- 确认模态框 ---------------- */
  function confirmDialog(opts) {
    return new Promise(function (resolve) {
      var back = document.createElement('div');
      back.className = 'modal-backdrop';
      back.innerHTML = '<div class="modal" role="dialog">' +
        '<div class="modal-icon ' + (opts.danger ? 'danger' : '') + '">' + icon(opts.danger ? 'trash' : 'sparkles') + '</div>' +
        '<h3>' + esc(opts.title || '确认操作') + '</h3>' +
        '<p>' + esc(opts.text || '') + '</p>' +
        '<div class="modal-actions">' +
        '<button class="btn btn-ghost" data-act="0">取消</button>' +
        '<button class="btn ' + (opts.danger ? 'btn-danger' : 'btn-primary') + '" data-act="1">' + esc(opts.confirmText || '确认') + '</button>' +
        '</div></div>';
      document.body.appendChild(back);
      requestAnimationFrame(function () { back.classList.add('show'); });
      function close(v) {
        back.classList.remove('show');
        setTimeout(function () { back.remove(); }, 200);
        document.removeEventListener('keydown', onKey);
        resolve(v);
      }
      function onKey(e) { if (e.key === 'Escape') close(false); if (e.key === 'Enter') close(true); }
      document.addEventListener('keydown', onKey);
      back.addEventListener('click', function (e) { if (e.target === back) close(false); });
      $$('[data-act]', back).forEach(function (b) {
        b.addEventListener('click', function () { close(b.getAttribute('data-act') === '1'); });
      });
    });
  }

  /* ---------------- 日期 / 阅读时长 ---------------- */
  function fmtDate(iso) { return String(iso || '').slice(0, 10); }
  function fmtRel(iso) {
    var d = new Date(iso + 'T00:00:00');
    var diff = Date.now() - d.getTime();
    var day = 86400000;
    if (diff < 0) return fmtDate(iso);
    if (diff < day) return '今天';
    if (diff < 2 * day) return '昨天';
    if (diff < 30 * day) return Math.floor(diff / day) + ' 天前';
    return fmtDate(iso);
  }
  function readingTime(text) {
    var plain = String(text || '').replace(/<[^>]+>/g, '').replace(/\s/g, '');
    var cjk = (plain.match(/[\u4e00-\u9fa5]/g) || []).length;
    var words = (plain.match(/[a-zA-Z0-9]+/g) || []).length;
    var mins = Math.max(1, Math.round(cjk / 350 + words / 220));
    return mins + ' 分钟';
  }

  /* ---------------- Markdown 迷你渲染器 ---------------- */
  function looksLikeHtml(s) {
    return /^\s*<(h\d|p|div|ul|ol|pre|blockquote|section|figure)/i.test(s || '');
  }
  function md2html(md) {
    var s = esc(md || '');
    s = s.replace(/```([\s\S]*?)```/g, function (m, code) {
      return '<pre><code>' + code.replace(/^\n/, '').replace(/\n$/, '') + '</code></pre>';
    });
    s = s.replace(/^###\s+(.*)$/gm, '<h3>$1</h3>')
      .replace(/^##\s+(.*)$/gm, '<h2>$1</h2>')
      .replace(/^#\s+(.*)$/gm, '<h2>$1</h2>')
      .replace(/^&gt;\s?(.*)$/gm, '<blockquote>$1</blockquote>')
      .replace(/^---+\s*$/gm, '<hr>');
    s = s.replace(/`([^`\n]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    s = s.replace(/((?:^- .*(?:\n|$))+)/gm, function (m) {
      return '<ul>' + m.trim().split('\n').map(function (l) { return '<li>' + l.replace(/^- /, '') + '</li>'; }).join('') + '</ul>';
    });
    s = s.replace(/((?:^\d+\. .*(?:\n|$))+)/gm, function (m) {
      return '<ol>' + m.trim().split('\n').map(function (l) { return '<li>' + l.replace(/^\d+\. /, '') + '</li>'; }).join('') + '</ol>';
    });
    return s.split(/\n{2,}/).map(function (block) {
      block = block.trim();
      if (!block) return '';
      if (/^<(h\d|ul|ol|pre|blockquote|hr)/.test(block)) return block;
      return '<p>' + block.replace(/\n/g, '<br>') + '</p>';
    }).join('\n');
  }
  function renderContent(post) {
    var c = post.content || '';
    return looksLikeHtml(c) ? c : md2html(c);
  }
  function highlight(text, q) {
    var t = esc(text);
    if (!q) return t;
    try {
      var re = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      return t.replace(re, '<mark>$1</mark>');
    } catch (e) { return t; }
  }

  /* ---------------- 文章卡片 ---------------- */
  function coverStyle(post) {
    return 'background:' + D.GRADIENTS[(post.cover || 0) % D.GRADIENTS.length];
  }
  function postCardH(post) {
    var sub = D.subOf(post.cat) || { name: post.cat };
    var iconName = (D.mainOf(post.cat) || {}).icon || 'file';
    return '<a class="post-card" href="article.html?id=' + post.id + '">' +
      '<div class="post-cover" style="' + coverStyle(post) + '">' +
        '<span class="cover-pattern"></span>' + icon(iconName, 'cover-icon') +
        '<span class="cover-cat">' + esc(sub.name) + '</span>' +
        '<span class="cover-like' + (D.isLiked(post.id) ? ' liked' : '') + '" data-like="' + post.id + '" title="点赞">' + icon('heart') + '</span>' +
      '</div>' +
      '<div class="post-info">' +
        '<div class="post-meta-top"><span class="badge badge-cat">' + esc(sub.name) + '</span><span>' + icon('clock') + ' ' + fmtDate(post.date) + '</span></div>' +
        '<h3 class="post-title">' + esc(post.title) + '</h3>' +
        '<p class="post-excerpt">' + esc(post.excerpt) + '</p>' +
        '<div class="post-meta">' +
          '<span>' + icon('eye') + ' ' + (post.views || 0) + '</span>' +
          '<span>' + icon('heart') + ' ' + (post.likes || 0) + '</span>' +
          '<span>' + icon('message') + ' ' + D.commentCount(post.id) + '</span>' +
          (post.status === 'draft' ? '<span class="badge badge-draft">草稿</span>' : '') +
          '<span class="read-more">阅读全文 ' + icon('arrow') + '</span>' +
        '</div>' +
      '</div>' +
    '</a>';
  }
  function postCardMini(post) {
    var sub = D.subOf(post.cat) || { name: post.cat };
    return '<a class="mini-card" href="article.html?id=' + post.id + '" style="' + coverStyle(post) + '">' +
      '<span class="cover-pattern"></span>' +
      '<span class="mini-cat">' + esc(sub.name) + '</span>' +
      '<strong>' + esc(post.title) + '</strong>' +
      '<span class="mini-date">' + fmtDate(post.date) + '</span>' +
    '</a>';
  }

  /* 卡片内的点赞按钮（事件委托，页面调用一次即可） */
  function bindCardLike(root) {
    (root || document).addEventListener('click', function (e) {
      var btn = e.target.closest('[data-like]');
      if (!btn) return;
      e.preventDefault();
      e.stopPropagation();
      var id = btn.getAttribute('data-like');
      Promise.resolve(D.toggleLike(id)).then(function (liked) {
        btn.classList.toggle('liked', liked);
        var post = D.getPost(id);
        if (post) {
          var num = btn.querySelector('.like-num');
          if (num) num.textContent = post.likes;
        }
        toast(liked ? '已点赞 ♥' : '已取消点赞', liked ? 'success' : 'info');
      });
    });
  }

  /* ---------- 页面启动：先加载数据（API/本地），再渲染 ---------- */
  function boot(cb) {
    D.prepare(function (apiOk) {
      init();
      if (cb) cb(apiOk);
    });
  }

  /* ---------------- 前台侧边栏 ---------------- */
  function renderSidebar() {
    var s = D.getSettings();
    var cats = D.getCats();
    var tags = D.tagCloud().slice(0, 18);
    var latestComments = D.allComments().slice(0, 4);
    var collected = D.getCollected();

    var catCount = {};
    D.getPosts().forEach(function (p) { catCount[p.cat] = (catCount[p.cat] || 0) + 1; });

    return '<aside class="sidebar">' +
      '<div class="card profile-card">' +
        '<div class="avatar avatar-lg" style="background:' + D.GRADIENTS[0] + '">' + esc(s.author.charAt(0)) + '</div>' +
        '<h3 class="profile-name">' + esc(s.author) + '</h3>' +
        '<p class="profile-sign">' + esc(s.sign) + '</p>' +
        '<div class="profile-actions">' +
          '<a class="btn btn-primary btn-sm" href="about.html">' + icon('user') + ' 关于我</a>' +
          '<a class="btn btn-ghost btn-sm" href="guestbook.html">' + icon('edit') + ' 留言板</a>' +
        '</div>' +
      '</div>' +
      '<div class="card" id="collectCard">' +
        '<h4 class="card-title">' + icon('star') + ' 我的收藏</h4>' +
        (collected.length
          ? '<div class="collect-list">' + collected.map(function (p) {
              return '<a class="collect-item" href="article.html?id=' + p.id + '">' + icon('file') + '<span>' + esc(p.title) + '</span></a>';
            }).join('') + '</div>'
          : '<p class="empty-tip">还没有收藏文章，点击文章页的 ☆ 试试</p>') +
      '</div>' +
      '<div class="card">' +
        '<h4 class="card-title">' + icon('archive') + ' 分类目录</h4>' +
        cats.map(function (c) {
          var total = c.subs.reduce(function (n, sub) { return n + (catCount[sub.id] || 0); }, 0);
          return '<div class="cat-group">' +
            '<a class="cat-main" href="category.html?main=' + c.id + '">' + icon(c.icon) + '<span>' + esc(c.name) + '</span><em>' + total + '</em></a>' +
            '<div class="cat-subs">' + c.subs.map(function (sub) {
              return '<a href="category.html?cat=' + sub.id + '">' + esc(sub.name) + '<em>' + (catCount[sub.id] || 0) + '</em></a>';
            }).join('') + '</div>' +
          '</div>';
        }).join('') +
      '</div>' +
      '<div class="card">' +
        '<h4 class="card-title">' + icon('tag') + ' 热门标签</h4>' +
        '<div class="tag-cloud">' + tags.map(function (t) {
          return '<a class="tag-chip" href="search.html?q=' + encodeURIComponent(t.tag) + '">' + esc(t.tag) + '<em>' + t.count + '</em></a>';
        }).join('') + '</div>' +
      '</div>' +
      '<div class="card">' +
        '<h4 class="card-title">' + icon('message') + ' 最新评论</h4>' +
        latestComments.map(function (c) {
          var p = D.getPost(c.postId);
          return '<a class="side-comment" href="article.html?id=' + c.postId + '#comments">' +
            '<span class="avatar avatar-xs" style="background:' + D.GRADIENTS[(c.color || 0) % D.GRADIENTS.length] + '">' + esc(c.name.charAt(0)) + '</span>' +
            '<span class="side-comment-body"><strong>' + esc(c.name) + '</strong>：' + esc(c.content.slice(0, 40)) + (c.content.length > 40 ? '…' : '') +
            '<em>——《' + esc(p ? p.title : '已删文章') + '》</em></span></a>';
        }).join('') +
      '</div>' +
    '</aside>';
  }

  /* ---------------- 管理后台外壳 ---------------- */
  var ADMIN_MENU = [
    { key: 'dashboard', label: '仪表盘', href: 'dashboard.html', icon: 'chart' },
    { key: 'posts', label: '文章管理', href: 'posts.html', icon: 'file' },
    { key: 'editor', label: '写文章', href: 'editor.html', icon: 'edit' },
    { key: 'comments', label: '评论管理', href: 'comments.html', icon: 'message' },
    { key: 'settings', label: '站点设置', href: 'settings.html', icon: 'sliders' }
  ];
  function mountAdmin(active, pageTitle) {
    if (!isAdmin()) {
      try { sessionStorage.setItem('linblog_after_login', location.pathname.split('/').pop() + location.search); } catch (e) {}
      location.replace('login.html');
      return;
    }
    var side = document.getElementById('adminSide');
    var top = document.getElementById('adminTop');
    var s = D.getSettings();
    if (side) {
      var pending = D.pendingCount();
      side.innerHTML =
        '<div class="admin-brand"><span class="logo-mark">' + esc(s.siteName.charAt(0)) + '</span><div><strong>' + esc(s.siteName) + '</strong><small>管理后台</small></div></div>' +
        '<nav class="admin-menu">' +
        ADMIN_MENU.map(function (m) {
          return '<a class="admin-menu-item' + (m.key === active ? ' active' : '') + '" href="' + m.href + '">' +
            icon(m.icon) + '<span>' + m.label + '</span>' +
            (m.key === 'comments' && pending ? '<em class="menu-badge">' + pending + '</em>' : '') + '</a>';
        }).join('') +
        '</nav>' +
        '<div class="admin-side-foot">' +
          '<a class="admin-menu-item" href="../index.html">' + icon('globe') + '<span>返回前台</span></a>' +
          '<button class="admin-menu-item logout-btn" id="adminLogout">' + icon('logout') + '<span>退出登录</span></button>' +
        '</div>';
      var lo = document.getElementById('adminLogout');
      if (lo) lo.addEventListener('click', function () {
        confirmDialog({ title: '退出登录', text: '确认退出管理后台吗？', confirmText: '退出' }).then(function (ok) {
          if (ok) { adminLogout(); location.href = 'login.html'; }
        });
      });
    }
    if (top) {
      top.innerHTML =
        '<h1 class="admin-page-title">' + esc(pageTitle) + '</h1>' +
        '<div class="admin-top-actions">' +
          '<form class="admin-search" id="adminSearch" action="../search.html" method="get">' + icon('search') +
            '<input type="text" name="q" placeholder="搜索全站文章…">' +
          '</form>' +
          '<a class="btn btn-ghost btn-sm" href="../index.html">' + icon('eye') + ' 查看网站</a>' +
          '<span class="avatar avatar-sm" style="background:' + D.GRADIENTS[0] + '" title="' + esc(s.author) + '">' + esc(s.author.charAt(0)) + '</span>' +
        '</div>';
    }
  }
  /* 存储不可用（如个别浏览器 file:// 限制）时退化为内存标记 */
  var adminFallback = false;
  function isAdmin() {
    try { return sessionStorage.getItem('linblog_admin') === '1'; } catch (e) { return adminFallback; }
  }
  function adminLogin() {
    adminFallback = true;
    try { sessionStorage.setItem('linblog_admin', '1'); } catch (e) {}
  }
  function adminLogout() {
    adminFallback = false;
    try { sessionStorage.removeItem('linblog_admin'); } catch (e) {}
  }

  /* ---------------- 其他 ---------------- */
  function bindBackTop() {
    var btn = document.createElement('button');
    btn.className = 'back-top';
    btn.id = 'backTop';
    btn.title = '返回顶部';
    btn.innerHTML = icon('arrow');
    document.body.appendChild(btn);
    btn.style.transform = 'rotate(-90deg)';
    window.addEventListener('scroll', function () {
      btn.classList.toggle('show', window.scrollY > 400);
    }, { passive: true });
    btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }
  function typewriter(el, text, speed) {
    if (!el) return;
    var i = 0;
    el.textContent = '';
    var cursor = document.createElement('span');
    cursor.className = 'tw-cursor';
    function tick() {
      if (i <= text.length) {
        el.textContent = text.slice(0, i);
        el.appendChild(cursor);
        i++;
        setTimeout(tick, speed || 60);
      } else {
        setTimeout(function () { cursor.remove(); }, 1200);
      }
    }
    tick();
  }
  function copyText(text, okMsg) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { toast(okMsg || '已复制到剪贴板'); },
        function () { fallbackCopy(text, okMsg); });
    } else fallbackCopy(text, okMsg);
  }
  function fallbackCopy(text, okMsg) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); toast(okMsg || '已复制到剪贴板'); }
    catch (e) { toast('复制失败，请手动复制', 'error'); }
    ta.remove();
  }

  /* 页面初始化公共动作 */
  function init() {
    applyAccent();
    renderHeader(document.body.getAttribute('data-page') || '');
    renderFooter();
    bindBackTop();
    bindCardLike(document);
  }

  return {
    $: $, $$: $$, esc: esc, getParam: getParam, icon: icon,
    renderHeader: renderHeader, renderFooter: renderFooter,
    toast: toast, confirmDialog: confirmDialog,
    fmtDate: fmtDate, fmtRel: fmtRel, readingTime: readingTime,
    md2html: md2html, looksLikeHtml: looksLikeHtml, renderContent: renderContent, highlight: highlight,
    coverStyle: coverStyle, postCardH: postCardH, postCardMini: postCardMini, renderSidebar: renderSidebar,
    mountAdmin: mountAdmin, isAdmin: isAdmin, adminLogin: adminLogin, adminLogout: adminLogout,
    toggleTheme: toggleTheme, setTheme: setTheme, applyAccent: applyAccent,
    typewriter: typewriter, copyText: copyText, init: init, boot: boot
  };
})();
