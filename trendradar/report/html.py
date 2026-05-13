# coding=utf-8
"""
HTML 报告渲染模块

提供 HTML 格式的热点新闻报告生成功能
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Callable

from trendradar.report.helpers import html_escape
from trendradar.utils.time import convert_time_for_display
from trendradar.ai.formatter import render_ai_analysis_html_rich


def render_html_content(
    report_data: Dict,
    total_titles: int,
    mode: str = "daily",
    update_info: Optional[Dict] = None,
    *,
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[List[Dict]] = None,
    rss_new_items: Optional[List[Dict]] = None,
    display_mode: str = "keyword",
    standalone_data: Optional[Dict] = None,
    ai_analysis: Optional[Any] = None,
    show_new_section: bool = True,
) -> str:
    """渲染HTML内容"""
    # 默认区域顺序
    default_region_order = ["hotlist", "rss", "new_items", "standalone", "ai_analysis"]
    if region_order is None:
        region_order = default_region_order

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>热点新闻分析</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js" integrity="sha512-BNaRQnYJYiPSqHHDb58B0yaPfCu+Wgds8Gp/gU33kqBtgNS4tSPHuGibyoeqMV/TJlSKda6FXzoEyYGjTe+vXA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                /* 深邃的暗黑背景，带微弱的科技蓝灰色调 */
                background: #0a0a0c;
                background-image: 
                    radial-gradient(circle at 50% 0%, #1a1a24 0%, transparent 50%),
                    radial-gradient(circle at 50% 100%, #110000 0%, transparent 50%);
                background-attachment: fixed;
                color: #e2e8f0;
                line-height: 1.6;
                -webkit-font-smoothing: antialiased;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                /* 毛玻璃高级质感 */
                background: rgba(20, 20, 22, 0.6);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 24px 48px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.05);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            .header {
                background: transparent;
                padding: 48px 32px;
                text-align: center;
                position: relative;
                /* 特斯拉红的微光底线 */
                box-shadow: inset 0 -2px 0 0 rgba(227, 25, 55, 0.8), 0 4px 20px rgba(227, 25, 55, 0.1);
            }

            .header-watermark { display: none; }

            .save-buttons {
                position: absolute;
                top: 20px;
                right: 24px;
                display: flex;
                gap: 12px;
                z-index: 10;
            }

            .save-btn, .save-dropdown-trigger, .toggle-wide-btn, .toggle-dark-btn {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #a0aec0;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 1px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .save-btn:hover, .toggle-wide-btn:hover, .toggle-dark-btn:hover {
                background: rgba(227, 25, 55, 0.1);
                border-color: #e31937;
                color: #fff;
                box-shadow: 0 0 12px rgba(227, 25, 55, 0.3);
            }

            .save-dropdown-menu { display: none; }

            .header-title {
                font-size: 32px;
                font-weight: 300;
                letter-spacing: 8px;
                text-transform: uppercase;
                margin: 0 0 32px 0;
                /* 金属反光质感文字 */
                background: linear-gradient(180deg, #ffffff 0%, #a0aec0 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .header-info {
                display: flex;
                justify-content: center;
                gap: 48px;
            }

            .info-item {
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .info-label {
                color: #64748b;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 8px;
            }

            .info-value {
                font-weight: 400;
                font-size: 20px;
                color: #f8fafc;
                font-family: 'SF Mono', Consolas, monospace;
            }

            .content { padding: 40px 32px; }

            /* AI 分析框 - 核心科技感 */
            .ai-section {
                margin-bottom: 48px;
                padding: 32px;
                background: linear-gradient(145deg, rgba(227, 25, 55, 0.03) 0%, rgba(0,0,0,0.4) 100%);
                border-radius: 12px;
                border: 1px solid rgba(227, 25, 55, 0.2);
                box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
                position: relative;
            }
            
            .ai-section::before {
                content: '';
                position: absolute;
                top: 0; left: 24px;
                width: 60px; height: 1px;
                background: #e31937;
                box-shadow: 0 0 10px #e31937;
            }

            .ai-section-header { margin-bottom: 24px; }

            .ai-section-title {
                font-size: 16px;
                font-weight: 500;
                letter-spacing: 3px;
                color: #e31937;
                text-transform: uppercase;
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .ai-block {
                margin-bottom: 24px;
                padding: 0;
                background: transparent;
                border: none;
                box-shadow: none;
            }

            .ai-block-title {
                font-size: 13px;
                font-weight: 600;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
            }
            
            .ai-block-title::before {
                content: '■';
                color: #e31937;
                margin-right: 8px;
                font-size: 10px;
            }

            .ai-block-content {
                font-size: 15px;
                line-height: 1.8;
                color: #cbd5e1;
                font-weight: 300;
                white-space: pre-wrap;
            }

            /* 新闻列表样式 */
            .word-header {
                border-bottom: 1px solid rgba(255,255,255,0.05);
                padding-bottom: 16px;
                margin-bottom: 24px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
            }

            .word-name {
                font-size: 22px;
                font-weight: 300;
                letter-spacing: 1px;
                color: #f8fafc;
            }

            .word-count {
                color: #64748b;
                font-size: 13px;
            }

            .news-item {
                padding: 20px 16px;
                margin-bottom: 8px;
                border-radius: 8px;
                background: rgba(255,255,255,0.02);
                border: 1px solid transparent;
                transition: all 0.3s ease;
                display: flex;
                gap: 20px;
                align-items: flex-start;
            }

            .news-item:hover {
                background: rgba(255,255,255,0.04);
                border-color: rgba(255,255,255,0.08);
                transform: translateX(4px);
            }

            .news-number {
                background: rgba(0,0,0,0.5);
                color: #64748b;
                border-radius: 6px;
                width: 28px; height: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'SF Mono', monospace;
                font-size: 12px;
                border: 1px solid rgba(255,255,255,0.05);
                transition: all 0.3s ease;
            }

            .news-item:hover .news-number {
                background: #e31937;
                color: #fff;
                border-color: #e31937;
                box-shadow: 0 0 12px rgba(227, 25, 55, 0.4);
            }

            .news-header { margin-bottom: 10px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }

            .source-name {
                color: #94a3b8;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
            }

            .keyword-tag {
                color: #e31937;
                font-size: 12px;
                font-weight: 500;
                background: rgba(227, 25, 55, 0.1);
                padding: 2px 6px;
                border-radius: 4px;
            }

            .rank-num {
                background: rgba(255,255,255,0.1);
                color: #e2e8f0;
                border-radius: 4px;
                padding: 2px 8px;
                font-family: 'SF Mono', monospace;
                font-size: 11px;
            }
            .rank-num.top { 
                background: rgba(227, 25, 55, 0.2); 
                color: #ff4d4d; 
                border: 1px solid rgba(227, 25, 55, 0.3);
            }
            .rank-num.high { 
                background: rgba(255, 255, 255, 0.15); 
                color: #fff; 
            }

            .time-info { color: #64748b; font-size: 12px; font-family: 'SF Mono', monospace; }

            .count-info {
                color: #e31937;
                font-size: 11px;
                font-weight: 500;
            }

            .news-title {
                font-size: 16px;
                font-weight: 400;
                line-height: 1.6;
                margin: 0;
            }

            .news-link {
                color: #e2e8f0;
                text-decoration: none;
                transition: color 0.2s;
            }

            .news-link:hover { color: #e31937; }

            .footer {
                background: rgba(0,0,0,0.4);
                border-top: 1px solid rgba(255,255,255,0.05);
                padding: 32px;
                text-align: center;
            }
            
            .footer-content {
                color: #475569;
                font-size: 12px;
                letter-spacing: 1px;
                text-transform: uppercase;
            }

            .footer-link {
                color: #94a3b8;
                text-decoration: none;
                transition: color 0.2s ease;
            }

            .footer-link:hover {
                color: #e31937;
            }

            .reading-progress {
                background: #e31937;
                height: 3px;
                box-shadow: 0 0 10px #e31937;
                position: fixed;
                top: 0; left: 0;
                width: 0;
                z-index: 9999;
                transition: width 0.1s linear;
            }
            
            .tab-bar, .search-bar, .fab-bar { display: none !important; }
            
            /* RSS 和 Standalone 样式适配暗黑科技风 */
            .rss-section { margin-top: 32px; padding-top: 24px; }
            .standalone-section { margin-top: 32px; padding-top: 24px; }
            
            .rss-section-header, .standalone-section-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
            }

            .rss-section-title, .standalone-section-title {
                font-size: 16px;
                font-weight: 500;
                letter-spacing: 3px;
                color: #e31937;
                text-transform: uppercase;
            }
            
            .rss-section-count, .standalone-section-count {
                color: #64748b;
                font-size: 14px;
            }

            .feed-group, .standalone-group { margin-bottom: 24px; }
            .feed-header, .standalone-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 12px;
                padding-bottom: 8px;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }

            .feed-name, .standalone-name { color: #f8fafc; font-size: 18px; font-weight: 300; }
            .feed-count, .standalone-count { color: #64748b; font-size: 13px; }

            .rss-item {
                background: rgba(255,255,255,0.02);
                border-left: 2px solid #e31937;
                border-radius: 4px;
                padding: 14px;
                margin-bottom: 12px;
                transition: all 0.3s ease;
            }
            
            .rss-item:hover {
                background: rgba(255,255,255,0.04);
                transform: translateX(4px);
            }

            .rss-meta { display: flex; gap: 12px; margin-bottom: 8px; align-items: center; flex-wrap: wrap; }
            .rss-time { color: #64748b; font-size: 12px; font-family: 'SF Mono', monospace; }
            .rss-author { color: #94a3b8; font-size: 12px; font-weight: 500; }
            
            .rss-title { font-size: 14px; line-height: 1.6; margin: 0; }
            .rss-title a { color: #e2e8f0; text-decoration: none; transition: color 0.2s; }
            .rss-title a:hover { color: #e31937; }

            .section-divider {
                margin-top: 32px;
                padding-top: 24px;
                border-top: 1px solid rgba(255,255,255,0.05);
            }

            .new-section { margin-top: 40px; padding-top: 24px; }
            .new-section-title {
                color: #f8fafc;
                font-size: 16px;
                font-weight: 600;
                margin: 0 0 20px 0;
            }
            .new-source-group { margin-bottom: 24px; }
            .new-source-title {
                color: #94a3b8;
                font-size: 13px;
                font-weight: 500;
                margin: 0 0 12px 0;
                padding-bottom: 6px;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }
            .new-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 0;
                border-bottom: 1px solid rgba(255,255,255,0.02);
            }
            .new-item:last-child { border-bottom: none; }
            .new-item-number {
                background: rgba(0,0,0,0.5);
                color: #64748b;
                border-radius: 4px;
                width: 24px; height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'SF Mono', monospace;
                font-size: 11px;
                flex-shrink: 0;
            }
            .new-item-rank {
                background: rgba(255,255,255,0.1);
                color: #e2e8f0;
                border-radius: 4px;
                padding: 2px 8px;
                font-family: 'SF Mono', monospace;
                font-size: 10px;
                flex-shrink: 0;
            }
            .new-item-rank.top { background: rgba(227, 25, 55, 0.2); color: #ff4d4d; }
            .new-item-rank.high { background: rgba(255, 255, 255, 0.15); color: #fff; }
            .new-item-content { flex: 1; min-width: 0; }
            .new-item-title { font-size: 14px; line-height: 1.5; color: #e2e8f0; margin: 0; }

            .error-section {
                background: rgba(227, 25, 55, 0.05);
                border: 1px solid rgba(227, 25, 55, 0.2);
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 24px;
            }
            .error-title { color: #ff4d4d; font-size: 14px; font-weight: 600; margin: 0 0 8px 0; }
            .error-list { list-style: none; padding: 0; margin: 0; }
            .error-item { color: #e31937; font-size: 13px; padding: 2px 0; font-family: 'SF Mono', monospace; }
        </style>
    </head>
    <body>
        <div class="reading-progress"></div>
        <div class="container">
            <div class="header">
                <div class="header-watermark">TrendRadar</div>
                <div class="save-buttons">
                    <button class="save-btn" onclick="saveAsImage()">导出报告</button>
                </div>
                <div class="header-title">热点新闻分析</div>
                <div class="header-info">
                    <div class="info-item">
                        <span class="info-label">报告类型</span>
                        <span class="info-value">"""

    # 处理报告类型显示（根据 mode 直接显示）
    if mode == "current":
        html += "当前榜单"
    elif mode == "incremental":
        html += "增量分析"
    else:
        html += "全天汇总"

    html += """</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">新闻总数</span>
                        <span class="info-value">"""

    html += f"{total_titles} 条"

    # 计算筛选后的热点新闻数量
    hot_news_count = sum(len(stat["titles"]) for stat in report_data["stats"])

    html += """</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">热点新闻</span>
                        <span class="info-value">"""

    html += f"{hot_news_count} 条"

    html += """</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">生成时间</span>
                        <span class="info-value">"""

    # 使用提供的时间函数或默认 datetime.now
    if get_time_func:
        now = get_time_func()
    else:
        now = datetime.now()
    html += now.strftime("%m-%d %H:%M")

    html += """</span>
                    </div>
                </div>
            </div>

            <div class="content">"""

    # 处理失败ID错误信息
    if report_data["failed_ids"]:
        html += """
                <div class="error-section">
                    <div class="error-title">⚠️ 请求失败的平台</div>
                    <ul class="error-list">"""
        for id_value in report_data["failed_ids"]:
            html += f'<li class="error-item">{html_escape(id_value)}</li>'
        html += """
                    </ul>
                </div>"""

    # 生成热点词汇统计部分的HTML
    stats_html = ""
    if report_data["stats"]:
        total_count = len(report_data["stats"])

        for i, stat in enumerate(report_data["stats"], 1):
            count = stat["count"]
            escaped_word = html_escape(stat["word"])

            stats_html += f"""
                <div class="word-group" data-tab-index="{i - 1}">
                    <div class="word-header">
                        <div class="word-name">{escaped_word}</div>
                        <div class="word-count">{count} 条</div>
                    </div>"""

            # 处理每个词组下的新闻标题，给每条新闻标上序号
            for j, title_data in enumerate(stat["titles"], 1):
                is_new = title_data.get("is_new", False)
                new_class = "new" if is_new else ""

                stats_html += f"""
                    <div class="news-item {new_class}">
                        <div class="news-number">{j}</div>
                        <div class="news-content">
                            <div class="news-header">"""

                # 根据 display_mode 决定显示来源还是关键词
                if display_mode == "keyword":
                    # keyword 模式：显示来源
                    stats_html += f'<span class="source-name">{html_escape(title_data["source_name"])}</span>'
                else:
                    # platform 模式：显示关键词
                    matched_keyword = title_data.get("matched_keyword", "")
                    if matched_keyword:
                        stats_html += f'<span class="keyword-tag">[{html_escape(matched_keyword)}]</span>'

                # 处理排名显示
                ranks = title_data.get("ranks", [])
                if ranks:
                    min_rank = min(ranks)
                    max_rank = max(ranks)
                    rank_threshold = title_data.get("rank_threshold", 10)

                    # 确定排名等级
                    if min_rank <= 3:
                        rank_class = "top"
                    elif min_rank <= rank_threshold:
                        rank_class = "high"
                    else:
                        rank_class = ""

                    if min_rank == max_rank:
                        rank_text = str(min_rank)
                    else:
                        rank_text = f"{min_rank}-{max_rank}"

                    stats_html += f'<span class="rank-num {rank_class}">{rank_text}</span>'

                # 处理时间显示
                time_display = title_data.get("time_display", "")
                if time_display:
                    # 简化时间显示格式，将波浪线替换为~
                    simplified_time = (
                        time_display.replace(" ~ ", "~")
                        .replace("[", "")
                        .replace("]", "")
                    )
                    stats_html += (
                        f'<span class="time-info">{html_escape(simplified_time)}</span>'
                    )

                # 处理出现次数
                count_info = title_data.get("count", 1)
                if count_info > 1:
                    stats_html += f'<span class="count-info">{count_info}次</span>'

                stats_html += """
                            </div>
                            <div class="news-title">"""

                # 处理标题和链接
                escaped_title = html_escape(title_data["title"])
                link_url = title_data.get("mobile_url") or title_data.get("url", "")

                if link_url:
                    escaped_url = html_escape(link_url)
                    stats_html += f'<a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
                else:
                    stats_html += escaped_title

                stats_html += """
                            </div>
                        </div>
                    </div>"""

            stats_html += """
                </div>"""

    # 给热榜统计添加外层包装
    if stats_html:
        stats_html = f"""
                <div class="hotlist-section">{stats_html}
                </div>"""

    # 生成新增新闻区域的HTML
    new_titles_html = ""
    if show_new_section and report_data["new_titles"]:
        new_titles_html += f"""
                <div class="new-section">
                    <div class="new-section-title">本次新增热点 (共 {report_data['total_new_count']} 条)</div>
                    <div class="new-sources-grid">"""

        for source_data in report_data["new_titles"]:
            escaped_source = html_escape(source_data["source_name"])
            titles_count = len(source_data["titles"])

            new_titles_html += f"""
                    <div class="new-source-group">
                        <div class="new-source-title">{escaped_source} · {titles_count}条</div>"""

            # 为新增新闻也添加序号
            for idx, title_data in enumerate(source_data["titles"], 1):
                ranks = title_data.get("ranks", [])

                # 处理新增新闻的排名显示
                rank_class = ""
                if ranks:
                    min_rank = min(ranks)
                    if min_rank <= 3:
                        rank_class = "top"
                    elif min_rank <= title_data.get("rank_threshold", 10):
                        rank_class = "high"

                    if len(ranks) == 1:
                        rank_text = str(ranks[0])
                    else:
                        rank_text = f"{min(ranks)}-{max(ranks)}"
                else:
                    rank_text = "?"

                new_titles_html += f"""
                        <div class="new-item">
                            <div class="new-item-number">{idx}</div>
                            <div class="new-item-rank {rank_class}">{rank_text}</div>
                            <div class="new-item-content">
                                <div class="new-item-title">"""

                # 处理新增新闻的链接
                escaped_title = html_escape(title_data["title"])
                link_url = title_data.get("mobile_url") or title_data.get("url", "")

                if link_url:
                    escaped_url = html_escape(link_url)
                    new_titles_html += f'<a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
                else:
                    new_titles_html += escaped_title

                new_titles_html += """
                                </div>
                            </div>
                        </div>"""

            new_titles_html += """
                    </div>"""

        new_titles_html += """
                    </div>
                </div>"""

    # 生成 RSS 统计内容
    def render_rss_stats_html(stats: List[Dict], title: str = "RSS 订阅更新") -> str:
        if not stats:
            return ""

        total_count = sum(stat.get("count", 0) for stat in stats)
        if total_count == 0:
            return ""

        rss_html = f"""
                <div class="rss-section">
                    <div class="rss-section-header">
                        <div class="rss-section-title">{title}</div>
                        <div class="rss-section-count">{total_count} 条</div>
                    </div>
                    <div class="rss-feeds-grid">"""

        for stat in stats:
            keyword = stat.get("word", "")
            titles = stat.get("titles", [])
            if not titles:
                continue

            keyword_count = len(titles)

            rss_html += f"""
                    <div class="feed-group">
                        <div class="feed-header">
                            <div class="feed-name">{html_escape(keyword)}</div>
                            <div class="feed-count">{keyword_count} 条</div>
                        </div>"""

            for title_data in titles:
                item_title = title_data.get("title", "")
                url = title_data.get("url", "")
                time_display = title_data.get("time_display", "")
                source_name = title_data.get("source_name", "")
                is_new = title_data.get("is_new", False)

                rss_html += """
                        <div class="rss-item">
                            <div class="rss-meta">"""

                if time_display:
                    rss_html += f'<span class="rss-time">{html_escape(time_display)}</span>'

                if source_name:
                    rss_html += f'<span class="rss-author">{html_escape(source_name)}</span>'

                if is_new:
                    rss_html += '<span class="rss-author" style="color: #e31937;">NEW</span>'

                rss_html += """
                            </div>
                            <div class="rss-title">"""

                escaped_title = html_escape(item_title)
                if url:
                    escaped_url = html_escape(url)
                    rss_html += f'<a href="{escaped_url}" target="_blank" class="rss-link">{escaped_title}</a>'
                else:
                    rss_html += escaped_title

                rss_html += """
                            </div>
                        </div>"""

            rss_html += """
                    </div>"""

        rss_html += """
                    </div>
                </div>"""
        return rss_html

    # 生成独立展示区内容
    def render_standalone_html(data: Optional[Dict]) -> str:
        if not data:
            return ""

        platforms = data.get("platforms", [])
        rss_feeds = data.get("rss_feeds", [])

        if not platforms and not rss_feeds:
            return ""

        total_platform_items = sum(len(p.get("items", [])) for p in platforms)
        total_rss_items = sum(len(f.get("items", [])) for f in rss_feeds)
        total_count = total_platform_items + total_rss_items

        if total_count == 0:
            return ""

        standalone_html = f"""
                <div class="standalone-section">
                    <div class="standalone-section-header">
                        <div class="standalone-section-title">独立展示区</div>
                        <div class="standalone-section-count">{total_count} 条</div>
                    </div>
                    <div class="standalone-groups-grid">"""

        group_idx = 0
        for platform in platforms:
            platform_name = platform.get("name", platform.get("id", ""))
            items = platform.get("items", [])
            if not items:
                continue

            standalone_html += f"""
                    <div class="standalone-group" data-standalone-tab="{group_idx}">
                        <div class="standalone-header">
                            <div class="standalone-name">{html_escape(platform_name)}</div>
                            <div class="standalone-count">{len(items)} 条</div>
                        </div>"""

            for j, item in enumerate(items, 1):
                title = item.get("title", "")
                url = item.get("url", "") or item.get("mobileUrl", "")
                rank = item.get("rank", 0)
                ranks = item.get("ranks", [])
                first_time = item.get("first_time", "")
                last_time = item.get("last_time", "")
                count = item.get("count", 1)

                standalone_html += f"""
                        <div class="news-item">
                            <div class="news-number">{j}</div>
                            <div class="news-content">
                                <div class="news-header">"""

                if ranks:
                    min_rank = min(ranks)
                    max_rank = max(ranks)
                    if min_rank <= 3:
                        rank_class = "top"
                    elif min_rank <= 10:
                        rank_class = "high"
                    else:
                        rank_class = ""
                    if min_rank == max_rank:
                        rank_text = str(min_rank)
                    else:
                        rank_text = f"{min_rank}-{max_rank}"
                    standalone_html += f'<span class="rank-num {rank_class}">{rank_text}</span>'
                elif rank > 0:
                    if rank <= 3:
                        rank_class = "top"
                    elif rank <= 10:
                        rank_class = "high"
                    else:
                        rank_class = ""
                    standalone_html += f'<span class="rank-num {rank_class}">{rank}</span>'

                if first_time and last_time and first_time != last_time:
                    first_time_display = convert_time_for_display(first_time)
                    last_time_display = convert_time_for_display(last_time)
                    standalone_html += f'<span class="time-info">{html_escape(first_time_display)}~{html_escape(last_time_display)}</span>'
                elif first_time:
                    first_time_display = convert_time_for_display(first_time)
                    standalone_html += f'<span class="time-info">{html_escape(first_time_display)}</span>'

                if count > 1:
                    standalone_html += f'<span class="count-info">{count}次</span>'

                standalone_html += """
                                </div>
                                <div class="news-title">"""

                escaped_title = html_escape(title)
                if url:
                    escaped_url = html_escape(url)
                    standalone_html += f'<a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
                else:
                    standalone_html += escaped_title

                standalone_html += """
                                </div>
                            </div>
                        </div>"""

            standalone_html += """
                    </div>"""
            group_idx += 1

        for feed in rss_feeds:
            feed_name = feed.get("name", feed.get("id", ""))
            items = feed.get("items", [])
            if not items:
                continue

            standalone_html += f"""
                    <div class="standalone-group" data-standalone-tab="{group_idx}">
                        <div class="standalone-header">
                            <div class="standalone-name">{html_escape(feed_name)}</div>
                            <div class="standalone-count">{len(items)} 条</div>
                        </div>"""

            for j, item in enumerate(items, 1):
                title = item.get("title", "")
                url = item.get("url", "")
                published_at = item.get("published_at", "")
                author = item.get("author", "")

                standalone_html += f"""
                        <div class="news-item">
                            <div class="news-number">{j}</div>
                            <div class="news-content">
                                <div class="news-header">"""

                if published_at:
                    try:
                        from datetime import datetime as dt
                        if "T" in published_at:
                            dt_obj = dt.fromisoformat(published_at.replace("Z", "+00:00"))
                            time_display = dt_obj.strftime("%m-%d %H:%M")
                        else:
                            time_display = published_at
                    except:
                        time_display = published_at

                    standalone_html += f'<span class="time-info">{html_escape(time_display)}</span>'

                if author:
                    standalone_html += f'<span class="source-name">{html_escape(author)}</span>'

                standalone_html += """
                                </div>
                                <div class="news-title">"""

                escaped_title = html_escape(title)
                if url:
                    escaped_url = html_escape(url)
                    standalone_html += f'<a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
                else:
                    standalone_html += escaped_title

                standalone_html += """
                                </div>
                            </div>
                        </div>"""

            standalone_html += """
                    </div>"""
            group_idx += 1

        standalone_html += """
                    </div>
                </div>"""
        return standalone_html

    rss_stats_html = render_rss_stats_html(rss_items, "RSS 订阅更新") if rss_items else ""
    rss_new_html = render_rss_stats_html(rss_new_items, "RSS 新增更新") if rss_new_items else ""
    standalone_html = render_standalone_html(standalone_data)
    ai_html = render_ai_analysis_html_rich(ai_analysis) if ai_analysis else ""

    region_contents = {
        "hotlist": stats_html,
        "rss": rss_stats_html,
        "new_items": (new_titles_html, rss_new_html),
        "standalone": standalone_html,
        "ai_analysis": ai_html,
    }

    def add_section_divider(content: str) -> str:
        if not content or 'class="' not in content:
            return content
        first_class_pos = content.find('class="')
        if first_class_pos != -1:
            insert_pos = first_class_pos + len('class="')
            return content[:insert_pos] + "section-divider " + content[insert_pos:]
        return content

    has_previous_content = False
    for region in region_order:
        content = region_contents.get(region, "")
        if region == "new_items":
            new_html, rss_new = content
            if new_html:
                if has_previous_content:
                    new_html = add_section_divider(new_html)
                html += new_html
                has_previous_content = True
            if rss_new:
                if has_previous_content:
                    rss_new = add_section_divider(rss_new)
                html += rss_new
                has_previous_content = True
        elif content:
            if has_previous_content:
                content = add_section_divider(content)
            html += content
            has_previous_content = True

    html += """
            </div>

            <div class="footer">
                <div class="footer-content">
                    POWERED BY <span style="color: #e31937; font-weight: 600;">TrendRadar</span> · 
                    <a href="https://github.com/sansan0/TrendRadar" target="_blank" class="footer-link">
                        GITHUB
                    </a>"""

    if update_info:
        html += f"""
                    <br>
                    <span style="color: #ff4d4d; font-weight: 500; margin-top: 8px; display: block;">
                        发现新版本 {update_info['remote_version']}，当前版本 {update_info['current_version']}
                    </span>"""

    html += """
                </div>
            </div>
        </div>

        <script>
            // 极简导出功能
            async function saveAsImage() {
                const button = event.target;
                const originalText = button.textContent;

                try {
                    button.textContent = 'GENERATING...';
                    button.disabled = true;
                    window.scrollTo(0, 0);

                    await new Promise(resolve => setTimeout(resolve, 200));

                    const buttons = document.querySelector('.save-buttons');
                    buttons.style.visibility = 'hidden';

                    await new Promise(resolve => setTimeout(resolve, 100));

                    const container = document.querySelector('.container');

                    const canvas = await html2canvas(container, {
                        backgroundColor: '#0a0a0c',
                        scale: 1.5,
                        useCORS: true,
                        allowTaint: false,
                        logging: false,
                        width: container.offsetWidth,
                        height: container.offsetHeight
                    });

                    buttons.style.visibility = 'visible';

                    const link = document.createElement('a');
                    const now = new Date();
                    const filename = `Tesla_Radar_${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}$${String(now.getDate()).padStart(2, '0')}_$${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}.png`;

                    link.download = filename;
                    link.href = canvas.toDataURL('image/png', 1.0);

                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    button.textContent = 'SAVED!';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);

                } catch (error) {
                    const buttons = document.querySelector('.save-buttons');
                    buttons.style.visibility = 'visible';
                    button.textContent = 'FAILED';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);
                }
            }

            document.addEventListener('DOMContentLoaded', function() {
                window.scrollTo(0, 0);
                // 阅读进度条
                var progressBar = document.querySelector('.reading-progress');
                if (progressBar) {
                    window.addEventListener('scroll', function() {
                        var h = document.documentElement.scrollHeight - window.innerHeight;
                        progressBar.style.width = (h > 0 ? (window.scrollY / h * 100) : 0) + '%';
                    });
                }
            });
        </script>
    </body>
    </html>
    """

    return html
