from fpdf import FPDF

class PASPManual(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PASP: Portable Android Statistics Program - User Manual', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_manual():
    pdf = PASPManual()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 40, 'PASP User Manual', 0, 1, 'C')
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, 'Version 0.3.5', 0, 1, 'C')
    pdf.ln(20)

    # Intro
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '1. Introduction', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'PASP is a lightweight, local statistical analysis tool designed for the terminal. It is optimized for mobile environments like Termux but works on any system with Python.')
    pdf.ln(5)

    # Installation
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '2. Installation', 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'General:', 0, 1)
    pdf.set_font('Courier', '', 10)
    pdf.cell(0, 10, 'pip install git+https://github.com/ppmena/pasp', 0, 1)
    pdf.ln(5)

    # Usage
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '3. Usage Styles', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'Style A: pasp data.csv --auto\nStyle B: pasp anova data.csv var group')
    pdf.ln(5)

    # Commands
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '4. Commands Reference', 0, 1)

    commands = [
        ('descriptives', 'Calculate mean, median, SD, and classify variables.'),
        ('ttest-one', 'One-sample T-test with normality checks.'),
        ('ttest-ind', 'Independent samples T-test with optional --plot.'),
        ('anova', 'One-way ANOVA with post-hoc comparisons.'),
        ('regression', 'Simple linear regression analysis.'),
        ('doctor', 'Check environment and dependencies.'),
        ('update', 'Update PASP to the latest version.')
    ]

    for cmd, desc in commands:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'- {cmd}:', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 8, desc)
        pdf.ln(2)

    # Examples
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '5. Examples with Built-in Datasets', 0, 1)

    examples = [
        'pasp examples/ejemplo_anova.csv --auto',
        'pasp examples/ejemplo_ttest.csv --ttest-ind recovery_time treatment --plot',
        'pasp examples/ejemplo_regresion.csv --regression exam_score hours_studied'
    ]

    for ex in examples:
        pdf.set_font('Courier', '', 10)
        pdf.multi_cell(0, 10, ex, border=1)
        pdf.ln(5)

    pdf.output('manual/manual.pdf')
    print("Manual PDF generated at manual/manual.pdf")

if __name__ == "__main__":
    generate_manual()
