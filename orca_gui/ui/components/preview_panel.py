"""Preview and validation panel."""

from __future__ import annotations

import html
import json

import streamlit as st

from orca_gui.core.input_generator import GeneratedInput


def _message_html(messages: list[str], css_class: str) -> str:
    if not messages:
        return ""
    rendered = "".join(
        f'<div class="orca-status {css_class}">{html.escape(message)}</div>'
        for message in messages
    )
    return rendered


def _preview_lines_html(generated: GeneratedInput) -> str:
    """Render preview lines with sea-themed directive highlighting."""
    if not generated.text:
        subject = "batch script preview" if generated.title == "Generated Batch Script" else "ORCA file preview"
        return f'<div class="orca-preview-empty">Complete the required inputs to generate a {subject}.</div>'

    rendered_lines: list[str] = []
    for raw_line in generated.text.rstrip().splitlines():
        escaped = html.escape(raw_line) or "&nbsp;"
        if generated.title == "Generated Batch Script":
            stripped = raw_line.lstrip()
            if stripped.startswith("###"):
                css_class = "orca-python-banner-line"
            elif stripped.startswith("#"):
                css_class = "orca-python-comment-line"
            elif raw_line.startswith('"""') or raw_line.startswith("'''"):
                css_class = "orca-python-docstring-line"
            elif stripped.startswith(("def ", "class ", "import ", "from ", "if __name__")):
                css_class = "orca-python-structure-line"
            else:
                css_class = "orca-code-line"
        else:
            if raw_line.startswith("!"):
                css_class = "orca-simple-line"
            elif raw_line.startswith("%") or raw_line.startswith("*"):
                css_class = "orca-directive-line"
            else:
                css_class = "orca-code-line"
        rendered_lines.append(f'<div class="{css_class}">{escaped}</div>')
    return "\n".join(rendered_lines)


def _status_html(generated: GeneratedInput) -> str:
    """Render validation status HTML."""
    if generated.validation.passed:
        status_html = '<div class="orca-status status-success">All checks passed.</div>'
    else:
        status_html = ""
    status_html += _message_html(generated.validation.errors, "status-error")
    status_html += _message_html(generated.validation.warnings, "status-warning")
    status_html += _message_html(generated.validation.infos, "status-info")
    return status_html


def _copy_action_html(generated: GeneratedInput) -> str:
    """Render a JS-backed copy button with transient status text."""
    if not generated.text:
        return ""
    button_id = f"orca-copy-{abs(hash((generated.title, generated.filename, generated.text))) :x}"
    status_id = f"{button_id}-status"
    copy_payload = json.dumps(generated.text)
    return f"""
    <div class="orca-preview-actions">
      <button id="{button_id}" class="copy-button" type="button">Copy Preview To Clipboard</button>
      <span class="copy-status" id="{status_id}" aria-live="polite"></span>
    </div>
    <style>
      .orca-preview-actions {{
        align-items: center;
        display: flex;
        gap: 0.75rem;
        margin: 0.2rem 0 0.4rem;
      }}
      .copy-button {{
        align-items: center;
        background: #53D2DC;
        border: none;
        border-radius: 12px;
        color: #0f2c3c;
        cursor: pointer;
        display: inline-flex;
        font-family: Arial, sans-serif;
        font-size: 0.98rem;
        font-weight: 600;
        justify-content: center;
        min-height: 42px;
        padding: 0.6rem 0.9rem;
      }}
      .copy-status {{
        color: #0f5132;
        font-family: Arial, sans-serif;
        font-size: 0.92rem;
        opacity: 0;
        transition: opacity 0.25s ease;
      }}
      .copy-status.visible {{
        opacity: 1;
      }}
    </style>
    <script>
      (() => {{
        const button = document.getElementById({json.dumps(button_id)});
        const status = document.getElementById({json.dumps(status_id)});
        if (!button || !status || button.dataset.bound === "1") {{
          return;
        }}
        button.dataset.bound = "1";
        button.addEventListener("click", async () => {{
          const text = {copy_payload};
          let copied = false;
          try {{
            const clipboard =
              navigator.clipboard ||
              (window.parent && window.parent.navigator && window.parent.navigator.clipboard);
            if (clipboard && clipboard.writeText) {{
              await clipboard.writeText(text);
              copied = true;
            }}
          }} catch (error) {{
            copied = false;
          }}
          if (!copied) {{
            const helper = document.createElement("textarea");
            helper.value = text;
            helper.setAttribute("readonly", "");
            helper.style.left = "-9999px";
            helper.style.position = "fixed";
            helper.style.top = "0";
            document.body.appendChild(helper);
            helper.focus();
            helper.select();
            helper.setSelectionRange(0, helper.value.length);
            copied = document.execCommand("copy");
            document.body.removeChild(helper);
          }}
          status.textContent = copied ? "Content copied" : "Copy failed";
          status.classList.add("visible");
          window.setTimeout(() => status.classList.remove("visible"), 1600);
        }});
      }})();
    </script>
    """


def render_preview_panel(generated: GeneratedInput) -> None:
    """Render sticky preview panel with validation status."""
    st.markdown(f"### {generated.title}")
    st.markdown(f'<div class="orca-preview-code">{_preview_lines_html(generated)}</div>', unsafe_allow_html=True)
    if generated.text:
        copy_col, download_col = st.columns([5, 1], gap="small")
        with copy_col:
            st.html(_copy_action_html(generated), unsafe_allow_javascript=True)
        with download_col:
            st.download_button(
                " ",
                data=generated.text,
                file_name=generated.filename,
                mime=generated.mime_type,
                key=f"download-{generated.title}-{generated.filename}",
                help="Download input file",
                icon=":material/download:",
                on_click="ignore",
                use_container_width=True,
            )
    st.markdown("### Validation Status")
    st.markdown(_status_html(generated), unsafe_allow_html=True)
