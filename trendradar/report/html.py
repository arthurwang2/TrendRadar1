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

            .news-header { margin-bottom: 10px; display: flex; gap: 12px; align-items: center; }

            .source-name {
                color: #94a3b8;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
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

            .time-info { color: #64748b; font-size: 12px; font-family: 'SF Mono', monospace; }

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

            .reading-progress {
                background: #e31937;
                height: 3px;
                box-shadow: 0 0 10px #e31937;
            }
            
            /* 隐藏原版多余组件 */
            .tab-bar, .search-bar, .fab-bar { display: none !important; }
