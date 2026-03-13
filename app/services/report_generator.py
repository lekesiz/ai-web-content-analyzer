"""PDF and JSON report generation."""

import json
from io import BytesIO
from fpdf import FPDF


class ReportGenerator:
    """Generates exportable reports from analysis data."""

    def generate_json(self, analysis_data):
        """Format analysis data as pretty-printed JSON."""
        return json.dumps(analysis_data, indent=2, ensure_ascii=False, default=str)

    def generate_pdf(self, analysis_data):
        """Generate PDF report."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Header
        pdf.set_font('Helvetica', 'B', 20)
        pdf.cell(0, 12, 'Web Content Analysis Report', new_x='LMARGIN', new_y='NEXT', align='C')
        pdf.ln(4)

        # URL and Date
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(100, 100, 100)
        url = analysis_data.get('url', 'N/A')
        pdf.cell(0, 6, f'URL: {url}', new_x='LMARGIN', new_y='NEXT')
        timestamp = analysis_data.get('timestamp', 'N/A')
        pdf.cell(0, 6, f'Date: {timestamp}', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(6)

        # Overall Score
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', 'B', 16)
        overall = analysis_data.get('overall_score', 0)
        pdf.cell(0, 10, f'Overall Score: {overall:.0f}/100', new_x='LMARGIN', new_y='NEXT', align='C')
        pdf.ln(4)

        # Sub-scores
        pdf.set_font('Helvetica', '', 12)
        scores = [
            ('SEO Score', analysis_data.get('seo_score', 0)),
            ('Content Score', analysis_data.get('content_score', 0)),
            ('Technical Score', analysis_data.get('technical_score', 0)),
        ]
        for label, score in scores:
            pdf.cell(0, 8, f'{label}: {score:.0f}/100', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(6)

        # Page Info
        self._add_section(pdf, 'Page Information')
        info_items = [
            ('Title', analysis_data.get('page_title', 'N/A')),
            ('Word Count', str(analysis_data.get('word_count', 0))),
            ('Language', (analysis_data.get('language') or 'N/A').upper()),
            ('Response Time', f'{analysis_data.get("response_time", 0):.2f}s'),
        ]
        for label, value in info_items:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(50, 7, f'{label}:', new_x='RIGHT')
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 7, str(value)[:80], new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

        # SEO Details
        seo = analysis_data.get('seo_details')
        if seo:
            self._add_section(pdf, 'SEO Analysis')
            seo_items = [
                ('Title Length', f'{seo.get("title_length", 0)} chars (Score: {seo.get("title_score", 0):.0f})'),
                ('Meta Description', f'{seo.get("meta_desc_length", 0)} chars (Score: {seo.get("meta_desc_score", 0):.0f})'),
                ('H1 Tags', str(seo.get('h1_count', 0))),
                ('H2 Tags', str(seo.get('h2_count', 0))),
                ('Images', f'{seo.get("img_total", 0)} total, {seo.get("img_without_alt", 0)} missing alt'),
                ('Internal Links', str(seo.get('internal_links', 0))),
                ('External Links', str(seo.get('external_links', 0))),
                ('Canonical URL', 'Yes' if seo.get('has_canonical') else 'No'),
                ('Open Graph Tags', 'Yes' if seo.get('has_og_tags') else 'No'),
            ]
            for label, value in seo_items:
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(50, 6, f'{label}:', new_x='RIGHT')
                pdf.set_font('Helvetica', '', 9)
                pdf.cell(0, 6, value, new_x='LMARGIN', new_y='NEXT')
            pdf.ln(4)

        # Issues
        issues = seo.get('issues', []) if seo else []
        if issues:
            self._add_section(pdf, 'Issues Found')
            pdf.set_font('Helvetica', '', 9)
            for issue in issues:
                severity = issue.get('severity', 'low').upper()
                message = issue.get('message', '')
                pdf.set_text_color(
                    200 if severity == 'HIGH' else (180 if severity == 'MEDIUM' else 100),
                    50 if severity == 'HIGH' else (130 if severity == 'MEDIUM' else 100),
                    50,
                )
                pdf.cell(0, 6, f'[{severity}] {message[:90]}', new_x='LMARGIN', new_y='NEXT')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(4)

        # AI Recommendations
        recs = analysis_data.get('ai_recommendations', [])
        if recs:
            self._add_section(pdf, 'AI Recommendations')
            pdf.set_font('Helvetica', '', 9)
            for rec in recs:
                priority = rec.get('priority', 'low').upper()
                title = rec.get('title', '')
                desc = rec.get('description', '')
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(0, 6, f'[{priority}] {title}', new_x='LMARGIN', new_y='NEXT')
                pdf.set_font('Helvetica', '', 8)
                # Word-wrap description
                pdf.multi_cell(0, 5, desc[:200])
                pdf.ln(2)

        # Footer
        pdf.ln(8)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, 'Generated by AI Web Content Analyzer - Universite de Strasbourg', align='C')

        return pdf.output()

    def _add_section(self, pdf, title):
        """Add a section header to the PDF."""
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(30, 64, 175)
        pdf.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        pdf.set_draw_color(30, 64, 175)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        pdf.set_text_color(0, 0, 0)
