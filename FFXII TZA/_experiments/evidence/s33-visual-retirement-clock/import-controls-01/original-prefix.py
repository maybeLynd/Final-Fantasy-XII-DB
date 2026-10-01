cwd = os.getcwd()
os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
os.chdir(cwd)
