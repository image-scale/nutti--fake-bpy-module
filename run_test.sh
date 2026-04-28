#!/bin/bash
set -eo pipefail

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export CI=true
export PYTHONPATH="/workspace/fake-bpy-module/src:/workspace/fake-bpy-module/tests/python/fake_bpy_module_test:${PYTHONPATH:-}"

cd /workspace/fake-bpy-module
pytest tests/python/fake_bpy_module_test/fake_bpy_module_test/ -v --tb=short -p no:cacheprovider \
  --deselect=tests/python/fake_bpy_module_test/fake_bpy_module_test/generator_test.py::WriterTestBase \
  --deselect=tests/python/fake_bpy_module_test/fake_bpy_module_test/transformer_test.py::ModuleStructureTest

