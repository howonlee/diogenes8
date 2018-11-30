from setuptools import setup

setup(
        name="diogenes8",
        version="1.0.0",
        description="A scheduler to remind you to talk to your friends",
        url="https://github.com/howonlee/diogenes8",
        author="Howon Lee",
        license="MIT",
        py_modules=["dio", "diocli"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Other Audience',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
        ],
        project_urls={
            'Documentation':"https://github.com/howonlee/diogenes8",
            'Source':"https://github.com/howonlee/diogenes8",
            'Tracker':"https://github.com/howonlee/diogenes8/issues",
        },
        python_requires='>3.7',
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
