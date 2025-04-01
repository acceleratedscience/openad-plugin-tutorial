"""
Centralized plugin parameters

- Exposed metadata from the yaml
- Snippets for repeated text in command descriptions
- Any other shared parameters
"""

import os
import yaml

# Load plugin_metadata.yml
plugin_metadata = {}
try:
    metadata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugin_metadata.yaml")
    with open(metadata_file, "r", encoding="utf-8") as f:
        plugin_metadata = yaml.safe_load(f)
except Exception:  # pylint: disable=broad-except
    pass

# Expose metadata
PLUGIN_NAME = plugin_metadata.get("name")
PLUGIN_KEY = PLUGIN_NAME.lower().replace(" ", "_")
PLUGIN_NAMESPACE = plugin_metadata.get("namespace")


# --- Edit below this line --- #
