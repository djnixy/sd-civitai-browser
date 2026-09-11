# AGENTS.md

## Overview
This repository contains the Civitai Helper / Civitai Browser+ extension for SD-WebUI and SD-WebUI Forge / Forge Classic (neo branch).

## Compatibility Guidelines

### SD-WebUI Forge Classic (neo) & SD-WebUI Compatibility
- Always maintain compatibility with [sd-webui-forge-classic (neo branch)](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo) as well as standard AUTOMATIC1111 SD-WebUI.
- **cmd_opts Safety**: Attributes on `cmd_opts` or `shared.cmd_opts` (e.g., `hypernetwork_dir`, `ckpt_dir`, `embeddings_dir`, `lora_dir`, `vae_dir`, `controlnet_dir`, `ui_config_file`) might not exist on the `argparse.Namespace` object in Forge Classic Neo.
  - In code logic, always access attributes on `cmd_opts` safely using `getattr(cmd_opts, 'attr_name', None)`.
  - Missing `cmd_opts` attributes are also safely initialized to `None` in `scripts/civitai_global.py` to prevent `AttributeError` from third-party or legacy calls to `shared.cmd_opts.<attr>`.

### Domain Handling (`civitai.red`)
- The active Civitai domain is retrieved via `get_domain()` in `scripts/civitai_api.py`.
- If the configured domain or requested endpoint is `civitai.com`, automatically map/redirect it to `civitai.red`.
- `request_civit_api()` and `get_download_link()` must automatically rewrite any `civitai.com` URLs to use `civitai.red`.
- JavaScript components retrieve the active domain from `#civitai_domain textarea` and map `civitai.com` to `civitai.red`.

### UI Components (Gradio 4+)
- Use `gr.update(...)` for component updates instead of deprecated component-specific update methods (e.g. `gr.Button.update(...)`).

## Key Files
- `scripts/civitai_global.py`: Global initialization, logging, and `cmd_opts` compatibility patches.
- `scripts/civitai_api.py`: Civitai API integration, `get_domain()`, and endpoint handling.
- `scripts/civitai_gui.py`: UI layout and setting definitions.
- `scripts/civitai_download.py`: Model download queue and aria2 RPC integration.
- `scripts/civitai_file_manage.py`: Model file management, scanning, and metadata handling.
- `javascript/civitai-html.js`: Frontend Javascript interactions.

## Testing & Verification
- Verify that `cmd_opts` missing attributes do not throw `AttributeError`.
- Verify that `get_domain()` returns `civitai.red` when domain is set to or defaults from `civitai.com`.
