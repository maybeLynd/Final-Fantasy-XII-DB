Original run01 failed at pefile import before retained inputs or producer tests.
Its exact driver/terminal are preserved. This analysis venv has Capstone, not
pefile; basePython has neither. Reuse the published1548d3896 python-deps/pefile and
ordlookup copies, verifying Git raw bytes before use. Actual driver verifies
imported pefile path, pins all dependency bytes, and sets bounded subprocess
PYTHONPATH. No installation or global environment mutation. Read this before retry.
