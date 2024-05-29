import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="0.9.8.8",
    company_name="Old Fashioned Software",
    file_description="Simple Database Driven Journaling Program",
    internal_name="MJournal",
    legal_copyright="© Old Fashioned Software. All rights reserved.",
    original_filename="MJournal.exe",
    product_name="MJournal"
)