all: OJ_L_202402847_CS_TXT.md OJ_L_202402847_EN_TXT.md

OJ_L_202402847_CS_TXT.md: ../source/cra/OJ_L_202402847_CS_TXT.html
	pandoc $< -o $@

OJ_L_202402847_EN_TXT.md: ../source/cra/OJ_L_202402847_EN_TXT.html
	pandoc $< -o $@

analysis: OJ_L_202402847_EN_TXT.md
	python3 analyze_cra.py OJ_L_202402847_EN_TXT.md
