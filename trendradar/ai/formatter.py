# coding=utf-8
"""
AI 分析结果格式化模块

将 AI 分析结果格式化为各推送渠道的样式
"""

import html as html_lib
import re
from .analyzer import AIAnalysisResult


def _escape_html(text: str) -> str:
    """转义 HTML 特殊字符，防止 XSS 攻击"""
    return html_lib.escape(text) if text else ""


def _format_list_content(text: str) -> str:
    """
    格式化列表内容，确保序号前有换行
    例如将 "1. xxx 2. yyy" 转换为:
    1. xxx
    2. yyy
    """
    if not text:
        return ""
    
    text = text.strip()
    text = re.sub(r'(\d+\.)\s*【([^】]+)】([:：]?)', r'\1 \2：', text)
    result = re.sub(r'(\d+)\.([^ \d])', r'\1. \2', text)
    result = re.sub(r'(?<=[^\n])\s+(\d+\.)(?!\d)', r'\n\1', result)
    result = re.sub(r'(?<=[^\n])(\d+\.\*\*)', r'\n\1', result)
    result = re.sub(r'([：:;,。；，])\s*(\d+\.)(?!\d)', r'\1\n\2', result)
    result = re.sub(r'([。！？；，、])\s*([a-zA-Z0-9\u4e00-\u9fa5]+(方面|领域)[:：])', r'\1\n\2', result)
    result = re.sub(r'(?<=\S)\n*(【[^】]+】)', r'\n\n\1', result)
    result = re.sub(r'(【[^】]+】)\n+([:：])', r'\1\2', result)
    result = re.sub(r'(【[^】]+】[:：]?)[ \t]*(?=[^\s:：])', r'\1\n', result)
    result = re.sub(r'(?<![:：】])\n(\d+\.)(?!\d)', r'\n\n\1', result)

    return result


def _format_standalone_summaries(summaries: dict) -> str:
    """格式化独立展示区概括为纯文本行，每个源名称单独一行"""
    if not summaries:
        return ""
    lines = []
    for source_name, summary in summaries.items():
        if summary:
            lines.append(f"[{source_name}]:\n{summary}")
    return "\n\n".join(lines)


def render_ai_analysis_markdown(result: AIAnalysisResult) -> str:
    """渲染为通用 Markdown 格式（Telegram、企业微信、ntfy、Bark、Slack）"""
    if not result.success:
        if result.skipped:
            return f"ℹ️ {result.error}"
        return f"⚠️ AI 分析失败: {result.error}"

    lines = ["**✨ AI 行业动向简报**", ""]

    if result.core_trends:
        lines.extend(["**关键事件**", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["**舆论风向争议**", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["**市场影响**", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["**RSS 深度洞察**", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["**团队启发**", _format_list_content(result.outlook_strategy), ""])

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            lines.extend(["**独立源点速览**", summaries_text])

    return "\n".join(lines)


def render_ai_analysis_feishu(result: AIAnalysisResult) -> str:
    """渲染为飞书卡片 Markdown 格式"""
    if not result.success:
        if result.skipped:
            return f"ℹ️ {result.error}"
        return f"⚠️ AI 分析失败: {result.error}"

    lines = ["**✨ AI 行业动向简报**", ""]

    if result.core_trends:
        lines.extend(["**关键事件**", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["**舆论风向争议**", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["**市场影响**", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["**RSS 深度洞察**", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["**团队启发**", _format_list_content(result.outlook_strategy), ""])

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            lines.extend(["**独立源点速览**", summaries_text])

    return "\n".join(lines)


def render_ai_analysis_dingtalk(result: AIAnalysisResult) -> str:
    """渲染为钉钉 Markdown 格式"""
    if not result.success:
        if result.skipped:
            return f"ℹ️ {result.error}"
        return f"⚠️ AI 分析失败: {result.error}"

    lines = ["### ✨ AI 行业动向简报", ""]

    if result.core_trends:
        lines.extend(["#### 关键事件", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["#### 舆论风向争议", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["#### 市场影响", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["#### RSS 深度洞察", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["#### 团队启发", _format_list_content(result.outlook_strategy), ""])

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            lines.extend(["#### 独立源点速览", summaries_text])

    return "\n".join(lines)


def render_ai_analysis_html(result: AIAnalysisResult) -> str:
    """渲染为 HTML 格式（邮件）"""
    if not result.success:
        if result.skipped:
            return f'<div class="ai-info">ℹ️ {_escape_html(result.error)}</div>'
        return f'<div class="ai-error">⚠️ AI 分析失败: {_escape_html(result.error)}</div>'

    html_parts = ['<div class="ai-analysis">', "<h3>✨ AI 行业动向简报</h3>"]

    if result.core_trends:
        content = _format_list_content(result.core_trends)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend(['<div class="ai-section">', "<h4>关键事件</h4>", f'<div class="ai-content">{content_html}</div>', "</div>"])

    if result.sentiment_controversy:
        content = _format_list_content(result.sentiment_controversy)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend(['<div class="ai-section">', "<h4>舆论风向争议</h4>", f'<div class="ai-content">{content_html}</div>', "</div>"])

    if result.signals:
        content = _format_list_content(result.signals)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend(['<div class="ai-section">', "<h4>市场影响</h4>", f'<div class="ai-content">{content_html}</div>', "</div>"])

    if result.rss_insights:
        content = _format_list_content(result.rss_insights)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend(['<div class="ai-section">', "<h4>RSS 深度洞察</h4>", f'<div class="ai-content">{content_html}</div>', "</div>"])

    if result.outlook_strategy:
        content = _format_list_content(result.outlook_strategy)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend(['<div class="ai-section ai-conclusion">', "<h4>团队启发</h4>", f'<div class="ai-content">{content_html}</div>', "</div>"])

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            summaries_html = _escape_html(summaries_text).replace("\n", "<br>")
            html_parts.extend(['<div class="ai-section">', "<h4>独立源点速览</h4>", f'<div class="ai-content">{summaries_html}</div>', "</div>"])

    html_parts.append("</div>")
    return "\n".join(html_parts)


def render_ai_analysis_plain(result: AIAnalysisResult) -> str:
    """渲染为纯文本格式"""
    if not result.success:
        if result.skipped:
            return result.error
        return f"AI 分析失败: {result.error}"

    lines = ["【✨ AI 行业动向简报】", ""]

    if result.core_trends:
        lines.extend(["[关键事件]", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["[舆论风向争议]", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["[市场影响]", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["[RSS 深度洞察]", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["[团队启发]", _format_list_content(result.outlook_strategy), ""])

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            lines.extend(["[独立源点速览]", summaries_text])

    return "\n".join(lines)


def render_ai_analysis_telegram(result: AIAnalysisResult) -> str:
    """渲染为 Telegram HTML 格式"""
    if not result.success:
        if result.skipped:
            return f"ℹ️ {_escape_html(result.error)}"
        return f"⚠️ AI 分析失败: {_escape_html(result.error)}"

    lines = ["<b>✨ AI 行业动向简报</b>", ""]

    if result.core_trends:
        lines.extend(["<b>关键事件</b>", _escape_html(_format_list_content(result.core_trends)), ""])

    if result.sentiment_controversy:
        lines.extend(["<b>舆论风向争议</b>", _escape_html(_format_list_content(result.sentiment_controversy)), ""])

    if result.signals:
        lines.extend(["<b>市场影响</b>", _escape_html(_format_list_content(result.signals)), ""])

    if result.rss_insights:
        lines.extend(["<b>RSS 深度洞察</b>", _escape_html(_format_list_content(result.rss_insights)), ""])

    if result.outlook_strategy:
        lines.extend(["<b>团队启发</b>", _escape_html(_format_list_content(result.outlook_strategy)), ""])

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            lines.extend(["<b>独立源点速览</b>", _escape_html(summaries_text)])

    return "\n".join(lines)


def get_ai_analysis_renderer(channel: str):
    """根据渠道获取对应的渲染函数"""
    renderers = {
        "feishu": render_ai_analysis_feishu,
        "dingtalk": render_ai_analysis_dingtalk,
        "wework": render_ai_analysis_markdown,
        "telegram": render_ai_analysis_telegram,
        "email": render_ai_analysis_html_rich,
        "ntfy": render_ai_analysis_markdown,
        "bark": render_ai_analysis_plain,
        "slack": render_ai_analysis_markdown,
    }
    return renderers.get(channel, render_ai_analysis_markdown)


def render_ai_analysis_html_rich(result: AIAnalysisResult) -> str:
    """渲染为丰富样式的 HTML 格式（HTML 报告用）"""
    if not result:
        return ""

    if not result.success:
        if result.skipped:
            return f"""
                <div class="ai-section">
                    <div class="ai-info">ℹ️ {_escape_html(str(result.error))}</div>
                </div>"""
        error_msg = result.error or "未知错误"
        return f"""
                <div class="ai-section">
                    <div class="ai-error">⚠️ AI 分析失败: {_escape_html(str(error_msg))}</div>
                </div>"""

    ai_html = """
                <div class="ai-section">
                    <div class="ai-section-header">
                        <div class="ai-section-title">✨ AI 行业动向简报</div>
                        <span class="ai-section-badge">AI</span>
                    </div>
                    <div class="ai-blocks-grid">"""

    if result.core_trends:
        content = _format_list_content(result.core_trends)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f"""
                    <div class="ai-block">
                        <div class="ai-block-title">关键事件</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>"""

    if result.sentiment_controversy:
        content = _format_list_content(result.sentiment_controversy)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f"""
                    <div class="ai-block">
                        <div class="ai-block-title">舆论风向争议</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>"""

    if result.signals:
        content = _format_list_content(result.signals)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f"""
                    <div class="ai-block">
                        <div class="ai-block-title">市场影响</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>"""

    if result.rss_insights:
        content = _format_list_content(result.rss_insights)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f"""
                    <div class="ai-block">
                        <div class="ai-block-title">RSS 深度洞察</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>"""

    if result.outlook_strategy:
        content = _format_list_content(result.outlook_strategy)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f"""
                    <div class="ai-block">
                        <div class="ai-block-title">团队启发</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>"""

    if result.standalone_summaries:
        summaries_text = _format_standalone_summaries(result.standalone_summaries)
        if summaries_text:
            summaries_html = _escape_html(summaries_text).replace("\n", "<br>")
            ai_html += f"""
                    <div class="ai-block">
                        <div class="ai-block-title">独立源点速览</div>
                        <div class="ai-block-content">{summaries_html}</div>
                    </div>"""

    ai_html += """
                    </div>
                </div>"""
    return ai_html
