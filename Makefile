styles:
	stylus -c stylus --out css
	@echo
	@echo "Built CSS from Stylus"

watch:
	stylus -w -c stylus --out css
