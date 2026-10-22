#!/usr/bin/env python3
"""Build both editions from MyST, and package a portable LaTeX manuscript."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "print"
NAME = "CS532_Textbook"


def run(args, cwd=ROOT):
    print("Running:", " ".join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=cwd, check=True)


def build(builder):
    executable = ROOT / ".venv/bin/teachbooks"
    if not executable.exists():
        found = shutil.which("teachbooks")
        if not found:
            raise RuntimeError("Install requirements.txt in .venv first; see BUILDING.md")
        executable = Path(found)
    run([executable, "build", "book", "--builder", builder, "--warningiserror", "--keep-going"])


def export_latex():
    build("latex")
    source = ROOT / "book/_build/latex"
    main = source / f"{NAME}.tex"
    if not main.is_file():
        raise RuntimeError(f"Expected manuscript was not generated: {main}")
    support = PRINT / "_support"
    support.mkdir(parents=True, exist_ok=True)
    images = PRINT / "images"
    images.mkdir(parents=True, exist_ok=True)
    # Sphinx has already given colliding asset basenames distinct export names.
    # Do not copy logs, caches, generated PDFs or per-build auxiliary state.
    for path in source.rglob("*"):
        if path == main or not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".eps"}:
            if path.stem != NAME:
                # Preserve subdirectories: generated figure paths can be nested.
                relative = path.relative_to(source)
                if relative.parts[0] == "images":
                    relative = Path(*relative.parts[1:])
                destination = images / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
        elif path.suffix.lower() in {".sty", ".cls", ".tex", ".ist", ".bst", ".bib"}:
            destination = support / path.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
    text = main.read_text()
    # LaTeX input@path finds bundled Sphinx classes/styles, even without Python.
    prefix = "% Generated from book/; edit the MyST source, then run make latex.\n"
    prefix += "\\makeatletter\\def\\input@path{{_support/}}\\makeatother\n"
    text = prefix + text
    # Front/reference chapters remain unnumbered; Lecture 1 starts Chapter 1.
    for caption in ("Before you begin", "Study and reference"):
        text = text.replace("\\part{" + caption + "}",
                            "\\setcounter{secnumdepth}{-1}\n\\part*{" + caption + "}"
                            "\\addcontentsline{toc}{part}{" + caption + "}")
    text = text.replace("\\part{Lectures 1–6}",
                        "\\setcounter{chapter}{0}\\setcounter{secnumdepth}{2}\n"
                        "\\part{Lectures 1–6}")
    text = text.replace("\\begin{document}",
                        "\\graphicspath{{images/}{_support/}}\n\\begin{document}", 1)
    (PRINT / f"{NAME}.tex").write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n")
    print(f"Exported one continuous manuscript: print/{NAME}.tex")


def compile_pdf():
    if not shutil.which("latexmk"):
        raise RuntimeError("latexmk is missing; install a full TeX distribution or use Overleaf.")
    run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", f"{NAME}.tex"], PRINT)


def bundle():
    target = PRINT / f"{NAME}_Source.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in (f"{NAME}.tex", f"{NAME}.pdf", "README.md", ".latexmkrc"):
            path = PRINT / name
            if path.exists():
                archive.write(path, name)
        for directory in (PRINT / "images", PRINT / "_support"):
            for path in sorted(directory.rglob("*")):
                if path.is_file() and path.name != ".gitkeep":
                    archive.write(path, path.relative_to(PRINT))
    print(f"Portable bundle: {target.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=["html", "latex", "pdf", "bundle", "all"])
    args = parser.parse_args()
    if args.target in {"html", "all"}:
        build("html")
    if args.target in {"latex", "pdf", "bundle", "all"}:
        export_latex()
    if args.target in {"pdf", "bundle", "all"}:
        compile_pdf()
    if args.target in {"bundle", "all"}:
        bundle()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        sys.exit(1)
