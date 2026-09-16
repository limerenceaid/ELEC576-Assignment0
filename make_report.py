"""
Build the Assignment 0 report PDF from the artifacts produced by the task scripts.
Run with:  python make_report.py
"""
import textwrap, datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Preformatted,
                                Image, PageBreak, KeepTogether)

# ----------------------------------------------------------------- config ---
STUDENT   = "Shirou Jing"
EMAIL     = "sj186@rice.edu"
GH_USER   = "__GITHUB_USERNAME__"
REPO_URL  = "__REPO_URL__"
OUT       = "ELEC576_Assignment0_Report.pdf"

INK, MUTED, RULE = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e"), colors.HexColor("#d8d7d2")
CODEBG = colors.HexColor("#f4f4f2")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold",
                    fontSize=15, leading=19, spaceBefore=16, spaceAfter=7, textColor=INK)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold",
                    fontSize=11, leading=14, spaceBefore=11, spaceAfter=5, textColor=INK)
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontName="Helvetica",
                      fontSize=9.5, leading=13.5, spaceAfter=7, textColor=INK)
NOTE = ParagraphStyle("NOTE", parent=BODY, fontSize=8.5, leading=12, textColor=MUTED)
CODE = ParagraphStyle("CODE", parent=ss["Code"], fontName="Courier", fontSize=7,
                      leading=8.4, textColor=INK, backColor=CODEBG,
                      borderPadding=5, spaceBefore=3, spaceAfter=8)
CODE_BIG = ParagraphStyle("CODE_BIG", parent=CODE, fontSize=8.2, leading=10.2)
TITLE = ParagraphStyle("TITLE", parent=ss["Title"], fontName="Helvetica-Bold",
                       fontSize=20, leading=25, textColor=INK, spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=BODY, fontSize=11, leading=15,
                     alignment=1, textColor=MUTED)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def code(text, style=CODE, width=None):
    """A monospace block; long lines are hard-wrapped so nothing overflows."""
    if width is None:
        # usable text width, minus the block's own padding, divided by Courier's
        # advance width (0.6 em) -> the exact character budget for this size
        usable = letter[0] - 1.8 * inch - 2 * style.borderPadding
        width = int(usable / (style.fontSize * 0.6)) - 1
    out = []
    for line in text.rstrip("\n").split("\n"):
        if len(line) <= width:
            out.append(line)
        else:
            indent = " " * (len(line) - len(line.lstrip()))
            out += textwrap.wrap(line, width=width, subsequent_indent=indent + "    ",
                                 break_long_words=True, break_on_hyphens=False) or [line]
    return Preformatted("\n".join(out), style)


def read(p):
    with open(p) as f:
        return f.read()


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.9 * inch, 0.55 * inch,
                      f"ELEC 576 / COMP 576 - Fall 2026 - Assignment 0 - {STUDENT}")
    canvas.drawRightString(letter[0] - 0.9 * inch, 0.55 * inch, str(doc.page))
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(0.9 * inch, 0.72 * inch, letter[0] - 0.9 * inch, 0.72 * inch)
    canvas.restoreState()


S = []          # story

# ------------------------------------------------------------ title page ---
S += [Spacer(1, 1.7 * inch),
      Paragraph("ELEC 576 / COMP 576 &mdash; Fall 2026", SUB),
      Spacer(1, 6),
      Paragraph("Assignment 0", TITLE),
      Spacer(1, 10),
      Paragraph(f"{STUDENT} &middot; {EMAIL}", SUB),
      Paragraph(datetime.date.today().strftime("%B %d, %Y"), SUB),
      Spacer(1, 0.9 * inch),
      Paragraph(
          "All six tasks were carried out on macOS 15.1 (Apple silicon, arm64) using a fresh "
          "Anaconda installation. Every command and every figure reproduced in this report was "
          "executed on that machine; the scripts that generate them are included in the GitHub "
          "repository linked in Task 6.", NOTE),
      PageBreak()]

# --------------------------------------------------------------- task 1 ----
S += [Paragraph("1&nbsp;&nbsp;Python Machine Learning Stack (Anaconda)", H1),
      Paragraph(
          "Anaconda was installed from the official <font face='Courier'>Anaconda3-2026.07-1-MacOSX-arm64.sh</font> "
          "installer into <font face='Courier'>~/anaconda3</font>, and <font face='Courier'>conda init zsh</font> "
          "was run so that <font face='Courier'>conda</font> is available in new shells. The installation "
          "provides conda 26.5.3 on Python 3.14.6, with 552 packages in the base environment.", BODY),
      Paragraph("Task 1 &mdash; output of <font face='Courier'>conda info</font>", H2),
      code(read("outputs/task1_conda_info.txt"), CODE_BIG)]

info_head = "\n".join(read("outputs/task1_conda_list.txt").split("\n")[:14])
S += [Paragraph(
        "As an additional check that the installation works, <font face='Courier'>conda list</font> "
        "returns the full package inventory. Its first lines are shown below; the complete listing "
        "(552 packages) is saved in the repository as "
        "<font face='Courier'>outputs/task1_conda_list.txt</font>.", BODY),
      code(info_head, CODE_BIG),
      PageBreak()]

# --------------------------------------------------------------- task 2 ----
S += [Paragraph("2&nbsp;&nbsp;Transition from MATLAB to Python", H1),
      Paragraph(
          "Task 2 asks for every Python command in the <i>Linear Algebra Equivalents</i> table of "
          "<i>NumPy for MATLAB Users</i> to be run in IPython. The table has 82 rows, and where a row "
          "lists several equivalent spellings (for example <font face='Courier'>np.ndim(a)</font> and "
          "<font face='Courier'>a.ndim</font>) every alternative was executed, for 161 IPython cells in total.", BODY),
      Paragraph(
          "The matrices are my own choice: <font face='Courier'>a</font>, <font face='Courier'>b</font>, "
          "<font face='Courier'>c</font>, <font face='Courier'>d</font> are 5&times;5 with entries drawn "
          "uniformly from [0,1) and rounded to two decimals, and <font face='Courier'>v</font> is a matching "
          "5-vector. Values in [0,1) were chosen deliberately so that the threshold rows "
          "(<font face='Courier'>a &gt; 0.5</font>) are non-trivial, and a fixed seed "
          "(<font face='Courier'>default_rng(576)</font>) makes the whole transcript reproducible.", BODY),
      Paragraph("Deviations from the table, and why", H2),
      Paragraph(
          "Seven rows cannot be run exactly as printed. Each is annotated in place in the transcript, "
          "and they are collected here:", BODY)]

devs = [
    ("Row 28, 30, 76, 77", "These assign or sort in place, which would corrupt <font face='Courier'>a</font> "
     "for every later row. A copy <font face='Courier'>a_orig</font> is kept and restored immediately "
     "afterwards; the restore is shown in the transcript rather than done silently."),
    ("Row 46", "The table prints <font face='Courier'>np.ix_(np.r_[0:9.],np.r_[0:6.]</font> &mdash; a missing "
     "closing parenthesis. Float indices also raise <font face='Courier'>IndexError</font>, since "
     "<font face='Courier'>np.ix_</font> requires integer or boolean arrays, so integer ranges are used."),
    ("Row 57, 58", "The table writes a bare <font face='Courier'>logical_and</font>; it is called as "
     "<font face='Courier'>np.logical_and</font>."),
    ("Row 59, 60", "Bitwise <font face='Courier'>&amp;</font> and <font face='Courier'>|</font> are not defined "
     "on float arrays, so a separate integer pair <font face='Courier'>ai</font>, "
     "<font face='Courier'>bi</font> is used."),
    ("Row 65", "The table gives prose (&ldquo;Solve a.T x.T = b.T instead&rdquo;) rather than a command; it is "
     "written out as <font face='Courier'>linalg.solve(a.T, b.T).T</font>."),
    ("Row 67, 73", "Cholesky and conjugate gradients need a positive definite system, so "
     "<font face='Courier'>spd = a @ a.T + 5*np.eye(5)</font> is used instead of "
     "<font face='Courier'>a</font>."),
    ("Row 80", "<font face='Courier'>np.ceil</font> returns a float and "
     "<font face='Courier'>signal.resample</font> requires an integer sample count, so the result is "
     "wrapped in <font face='Courier'>int(...)</font>."),
    ("Row 82", "<font face='Courier'>a</font> has no singleton dimensions, so a 1&times;3&times;1&times;4 array "
     "is used to show what <font face='Courier'>squeeze</font> actually does."),
]
for label, why in devs:
    S.append(Paragraph(f"<b>{label}.</b> {why}", NOTE))

S += [Spacer(1, 6),
      Paragraph(
          "The full IPython transcript follows. It was produced by "
          "<font face='Courier'>task2_linalg.py</font>, which drives a real "
          "<font face='Courier'>InteractiveShell</font> so the <font face='Courier'>In[ ]</font> / "
          "<font face='Courier'>Out[ ]</font> pairs below are genuine IPython output.", BODY),
      PageBreak()]

# the transcript, split at row separators so pages break at natural points
transcript = read("outputs/task2_transcript.txt")
chunks, buf = [], []
for line in transcript.split("\n"):
    if line.startswith("=" * 20) and buf and buf[-1].strip() == "":
        chunks.append("\n".join(buf)); buf = []
    buf.append(line)
chunks.append("\n".join(buf))
for ch in chunks:
    if ch.strip():
        S.append(code(ch))

# --------------------------------------------------------------- task 3 ----
S += [PageBreak(),
      Paragraph("3&nbsp;&nbsp;Plotting &mdash; the given script", H1),
      Paragraph("Task 3 &mdash; the assignment's script, run verbatim in IPython", H2),
      code("import matplotlib.pyplot as plt\n"
           "plt.plot([1,2,3,4], [1,2,7,14])\n"
           "plt.axis([0, 6, 0, 20])\n"
           "plt.show()", CODE_BIG),
      Paragraph(
          "The figure it produces is below. To capture it to a file the script was run under the "
          "non-interactive <font face='Courier'>Agg</font> backend and followed by "
          "<font face='Courier'>plt.savefig(...)</font>; the four lines above are otherwise untouched. "
          "Under <font face='Courier'>Agg</font>, <font face='Courier'>plt.show()</font> emits a "
          "<font face='Courier'>UserWarning</font> that it cannot display interactively, which is expected "
          "and does not affect the figure.", BODY),
      Spacer(1, 4),
      Image("figures/task3.png", width=4.4 * inch, height=3.23 * inch),
      PageBreak()]

# --------------------------------------------------------------- task 4 ----
S += [Paragraph("4&nbsp;&nbsp;Plotting &mdash; a figure of my own", H1),
      Paragraph(
          "For Task 4 I plotted the three classical activation functions against their derivatives, "
          "which is the clearest single picture of why deep networks moved away from sigmoid. The left "
          "panel shows the functions; the right panel shows the gradients that backpropagation actually "
          "multiplies together. Sigmoid's derivative peaks at 0.25 and decays to zero in both tails, so a "
          "product of many such factors vanishes exponentially with depth. ReLU's derivative is exactly 1 "
          "on the positive half-line, so the gradient passes through unattenuated.", BODY),
      Spacer(1, 4),
      Image("figures/task4.png", width=6.5 * inch, height=2.73 * inch),
      Spacer(1, 8),
      Paragraph("Code", H2),
      code(read("task4_plot.py"), CODE)]

# ------------------------------------------------------------ task 5 & 6 ---
S += [PageBreak(),
      Paragraph("5&nbsp;&nbsp;Version Control System (GitHub)", H1),
      Paragraph("Task 5 &mdash; my VCS account", H2),
      code(f"GitHub username:  {GH_USER}\nProfile:          https://github.com/{GH_USER}", CODE_BIG),
      Paragraph(
          "The account is registered with my Rice address and has been upgraded through the GitHub "
          "Student Developer Pack for free private repositories.", BODY),

      Paragraph("6&nbsp;&nbsp;Integrated Development Environment", H1),
      Paragraph(
          "The project for this assignment was created and run as a standard Python project against the "
          "Anaconda interpreter installed in Task 1, then committed and pushed to GitHub as a public "
          "repository.", BODY),
      Paragraph("Task 6 &mdash; link to the project", H2),
      code(f"{REPO_URL}", CODE_BIG),
      Paragraph("The repository contains everything used to produce this report:", BODY),
      code("Assignment0/\n"
           "  task2_linalg.py      all 82 rows of the Linear Algebra Equivalents table\n"
           "  task3_plot.py        the assignment's plotting script\n"
           "  task4_plot.py        the activation-function figure\n"
           "  make_report.py       builds this PDF from the outputs below\n"
           "  outputs/\n"
           "    task1_conda_info.txt   conda info\n"
           "    task1_conda_list.txt   conda list, all 552 packages\n"
           "    task2_transcript.txt   the full IPython transcript\n"
           "  figures/\n"
           "    task3.png\n"
           "    task4.png", CODE_BIG)]

# --------------------------------------------------------------- sources ---
S += [Paragraph("Sources", H1),
      Paragraph(
          "NumPy developers, <i>NumPy for MATLAB Users</i>, "
          "https://numpy.org/doc/stable/user/numpy-for-matlab-users.html &mdash; the source of the "
          "&ldquo;Linear Algebra Equivalents&rdquo; table reproduced in Task 2.", NOTE),
      Paragraph(
          "The Matplotlib development team, <i>Pyplot Tutorial</i>, "
          "https://matplotlib.org/stable/tutorials/pyplot.html &mdash; background for Tasks 3 and 4.", NOTE),
      Paragraph(
          "Anaconda Inc., <i>Installing on macOS</i>, "
          "https://docs.anaconda.com/anaconda/install/mac-os/ &mdash; installation procedure for Task 1.", NOTE),
      Paragraph(
          "The Task 3 script is quoted from the assignment handout. All other code in this report is my own.", NOTE)]

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
                        title=f"ELEC 576 Assignment 0 - {STUDENT}", author=STUDENT)
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print(f"wrote {OUT}")
