import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hsbalance",
    version="0.0.32-a",
    author="Maged M.Eltorkoman",
    author_email="newmaged@gmail.com",
    description="Python tools for Practical Modeling and Solving High Speed Rotor Unbalance Problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing',
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    install_requires=['cvxpy>=1.1.18', 'pandas>=1.3.5'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
