"""Generate a curated ORCA 6.1 manual excerpt corpus for the GUI."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FragmentSpec:
    """A single snippet to locate within the extracted PDF text."""

    label: str
    phrase: str
    before: int
    after: int


@dataclass(frozen=True)
class SectionSpec:
    """A curated section for the output document."""

    title: str
    summary: str
    fragments: tuple[FragmentSpec, ...]


SECTIONS: tuple[SectionSpec, ...] = (
    SectionSpec(
        title="Input Structure and XYZ File Syntax",
        summary="General input structure for external XYZ files and the exact `* xyzfile` form used by this GUI.",
        fragments=(
            FragmentSpec("General xyzfile syntax", "* xyzfile Charge Multiplicity Filename", 2, 4),
            FragmentSpec("Example xyzfile usage", "* xyzfile 1 2 mycoords.xyz", 2, 2),
        ),
    ),
    SectionSpec(
        title="Parallel and Memory Controls",
        summary="Excerpt-backed syntax for `%pal nprocs` and `%maxcore`.",
        fragments=(
            FragmentSpec("Parallel block", "%pal nprocs 4 end # any number (positive integer)", 2, 4),
            FragmentSpec("Global MaxCore", "%MaxCore 2000", 2, 5),
        ),
    ),
    SectionSpec(
        title="SCF Convergence Controls",
        summary="The curated UI currently exposes simple convergence presets such as `TightSCF` and `VeryTightSCF`.",
        fragments=(
            FragmentSpec("TightSCF keyword context", "Tight (!TightSCF)", 2, 4),
            FragmentSpec("SCF block example", "%scf", 0, 5),
        ),
    ),
    SectionSpec(
        title="Geometry Optimization and Frequency Keywords",
        summary="Simple input keywords used for optimization and frequency jobs in the first milestone.",
        fragments=(
            FragmentSpec("Optimization keywords", "!LooseOpt, !OPT (default), !TightOpt, and !VeryTightOpt.", 2, 4),
            FragmentSpec("Frequency keyword table entry", "freq                                                     Vibrational frequencies", 2, 2),
        ),
    ),
    SectionSpec(
        title="DEFGRID Guidance",
        summary="Manual-backed default and override guidance for `DEFGRID1`, `DEFGRID2`, and `DEFGRID3`.",
        fragments=(
            FragmentSpec("DEFGRID overview", "develop three new grid schemes named: DEFGRID1, DEFGRID2 and DEFGRID3", 2, 6),
            FragmentSpec("How to change the default", "In order to change from the default DEFGRID2", 0, 4),
        ),
    ),
    SectionSpec(
        title="DFT Functional Keywords",
        summary="Curated functional entries used by the GUI method selector.",
        fragments=(
            FragmentSpec("GGA functionals", "BP86 [198, 199]", 0, 8),
            FragmentSpec("Hybrid functionals", "B3LYP         B3LYP    20", 2, 8),
            FragmentSpec("Range-separated hybrid example", "CAM-B3LYP [242]", 0, 2),
        ),
    ),
    SectionSpec(
        title="Basis-set Keywords",
        summary="Curated basis-set entries used by the GUI basis-set selector.",
        fragments=(
            FragmentSpec("Karlsruhe basis sets", "def2-SVP                 H–Rn", 0, 10),
            FragmentSpec("Correlation-consistent basis sets", "cc-pVDZ                   H–Ar, Ca–Kr", 0, 4),
        ),
    ),
    SectionSpec(
        title="CPCM Input Syntax",
        summary="Exact simple input and `%cpcm` block spellings used by the curated solvation controls.",
        fragments=(
            FragmentSpec("Simple CPCM invocation", "! CPCM(solvent)", 2, 4),
            FragmentSpec("Simple CPCMC invocation", "!CPCMC(solvent).", 2, 2),
            FragmentSpec("Simple SMD invocation", "! SMD(solvent)", 0, 5),
            FragmentSpec("Simple COSMORS invocation", "!COSMORS(Acetonitrile)", 2, 2),
            FragmentSpec("Solvation block keywords", 'solvent                "water"', 0, 6),
            FragmentSpec("Default Gaussian vdW surface", "surfacetype vdw_gaussian", 2, 4),
            FragmentSpec("SES point-charge surface", "surfacetype gepol_ses", 2, 3),
            FragmentSpec("Sample solvent availability", "acetonitrile / mecn / ch3cn                        X         X        X            X", 0, 5),
        ),
    ),
    SectionSpec(
        title="TDDFT and NACME Syntax",
        summary="Exact `%tddft` spellings for `nroots`, `iroot`, `nacme true`, and `etf true`.",
        fragments=(
            FragmentSpec("TDDFT NACME example", "NACME   TRUE", 4, 8),
            FragmentSpec("ETF extension", "ETF      TRUE", 4, 6),
            FragmentSpec("TDDFT grid overrides", "%TDDFT # or %CIS, they are equivalent", 0, 8),
        ),
    ),
    SectionSpec(
        title="Molecular Dynamics Activation",
        summary="Phase-gated reference showing that `MD` belongs on the simple input line and capturing the current curated `%md` commands used by the GUI.",
        fragments=(
            FragmentSpec("MD activation rule", "The molecular dynamics module is activated by specifying “MD” in the simple input line.", 0, 10),
            FragmentSpec("MD block overview", "Table 7.1: Overview of commands in the %md block", 3, 2),
            FragmentSpec("MD restart example", "Restart IfExists", 4, 4),
            FragmentSpec("Molecular dynamics print level", "The default value is Medium.", 4, 2),
            FragmentSpec("Molecular dynamics randomize", "Without a call to Randomize, a seed of 1 is always used.", 6, 2),
            FragmentSpec("Molecular dynamics SCF log control", "The default value is Append. Note that this can lead to large log files in long runs.", 6, 1),
            FragmentSpec("Molecular dynamics thermostat syntax", "Mandatory Arguments:            type            Keyword      { Berendsen, CSVR, NHC, None }", 0, 12),
            FragmentSpec("Molecular dynamics NHC defaults", "The Chain, MTS, and Yoshida modifiers only apply to NHC thermostats.", 0, 6),
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Generate curated ORCA 6.1 manual excerpts.")
    parser.add_argument("--pdf", required=True, type=Path, help="Path to the ORCA 6.1 manual PDF.")
    parser.add_argument("--output", required=True, type=Path, help="Output markdown file path.")
    return parser.parse_args()


def extract_pdf_text(pdf_path: Path) -> list[list[str]]:
    """Return the PDF text split into pages and lines."""
    command = ["pdftotext", "-layout", str(pdf_path), "-"]
    result = subprocess.run(command, capture_output=True, text=False, check=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    return [page.splitlines() for page in stdout.split("\f")]


def find_fragment(pages: list[list[str]], spec: FragmentSpec) -> tuple[int, str]:
    """Locate the first matching fragment in the PDF text."""
    for page_number, page_lines in enumerate(pages, start=1):
        for line_index, line in enumerate(page_lines):
            if spec.phrase in line:
                start = max(0, line_index - spec.before)
                end = min(len(page_lines), line_index + spec.after + 1)
                snippet = "\n".join(page_lines[start:end]).rstrip()
                return page_number, snippet
    raise ValueError(f"Could not find required manual phrase: {spec.phrase}")


def format_markdown(pages: list[list[str]], pdf_path: Path) -> str:
    """Build the output markdown document."""
    lines = [
        "# ORCA 6.1 Manual Excerpts",
        "",
        "> Auto-generated by `scripts/generate_manual_excerpts.py`.",
        f"> Source PDF: `{pdf_path.name}`",
        "",
        "This excerpt corpus is the single source of truth for the current GUI milestone.",
        "",
    ]
    for section in SECTIONS:
        lines.append(f"## {section.title}")
        lines.append("")
        lines.append(section.summary)
        lines.append("")
        for fragment in section.fragments:
            page_number, snippet = find_fragment(pages, fragment)
            lines.append(f"### {fragment.label}")
            lines.append("")
            lines.append(f"- PDF page: {page_number}")
            lines.append("")
            lines.append("```text")
            lines.append(snippet)
            lines.append("```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    pages = extract_pdf_text(args.pdf)
    output = format_markdown(pages, args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
