from setuptools import setup

setup(
        name="diogenes8",
        version="1.0.0",
        py_modules=["dio", "diocli"],
        install_requires=[
            "pyfakefs",
            "pytest",
            "hypothesis",
            "click",
            "python-crontab",
        ],
        entry_points = """
        [console_scripts]
        dio=diocli:cli
        """,
        )
