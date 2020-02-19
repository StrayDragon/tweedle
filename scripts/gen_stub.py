tplt = """
name="{{ external_app_name }}}"

[config_management]
# Used for check exist configs
find_exist_ordered_paths = [
  {{ path for path in paths }}
]
"""
