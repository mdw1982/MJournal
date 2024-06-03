import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="vfileDBBackup.txt",
    version="0.9.8.8",
    company_name="Old Fashioned Software",
    file_description="Simple Database Driven Journaling Program",
    internal_name="dbbackup",
    legal_copyright="© Old Fashioned Software. All rights reserved.",
    original_filename="dbbackup",
    product_name="MJournal"
)