# DirectoryBackupCapsule
A personal project that I hope will be useful to others. The Python script generates a backup capsule of a user defined size, starting from a user defined time.

# =============Disclaimer================
THIS PROJECT IS STILL A WORK IN PROGRESS. CHANGES SHALL BE MADE WITHOUT GIVING NOTICE. PERSONAL USE ONLY AT YOUR OWN RISK

# =============HOW TO USE IT=============
varSizeBackupCapsule has 3 operating modes (-excMode) OPTIONAL FLAG: auto, manual, debug.

	- auto: the program execute without explicit user input. requires varSizeBackupConfig.txt for configuration. This is the mode I use most of the time integrated with Crontab on a RaspianOS.

	- manual: the program when operated in this mode requires user input for backup directory, backup size, and backup capsule directory name

	- debug: the program when operating in this mode is basically the manual mode, and also prints out information useful for debugging debugging

alternative backup configuration file (-configFile) OPTIONAL FLAG: varSizeBackupConfig.txt is the default backup configuration file if -configFile is not defined 

# ============Configuration Files================
ExampleDirectoryDisc1meta.txt

	-this file defines the starting file creation/(last modified) epoch time of the backup capsule, when the backup directory is yet to be constructed.

	-This file will be populated with all original directory paths of the files backed up in the backup capsule directory capsule directory. the last
	 line will be epoch time of the last file that made it into the backup capsule

varSizeBackupConfig.txt

	-1st line (directory path): Backup files source directory (ExampleDirectory)
	-2nd line (directory path): Backup Capsule Target directory. If the define target directory (ExampleDirectoryDisc1) doesn't exist, one will be created automatically with executing the varSizeBackupCapsule
	-3rd line (number): Backup Capsule directory size in byte. (50050629632 = 50GB, a dual-layer Blu-Ray). This user defined, it can be as big or small as one wish.
	-4th line (file name): Backup Capsule meta starter filenames. see ExampleDirectoryDisc1meta.txt for specifics
