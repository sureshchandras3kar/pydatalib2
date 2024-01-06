from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='PyDataLib2',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add any dependencies here
    ],
    author='Suresh Chandra Sekar',  # noqa
    maintainer='Nithesh',  # noqa
    description='PyDataLib2 is a utilities igniting innovation and efficiency in development.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sureshchandras3kar/PyDataLib2',
    license='MIT',
    python_requires='>=3.6',
    keywords=[
        'python',
        'utilities',
        'development',
        'efficiency',
        'innovation',
        'data processing',
        'text manipulation',
        'file management',
        'data structures'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
