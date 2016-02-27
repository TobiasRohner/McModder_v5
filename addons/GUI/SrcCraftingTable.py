# -*- coding: utf-8 -*-
recipeShapeless = """GameRegistry.addShapelessRecipe(<output>, <imputs>);"""

recipe2x2 = """GameRegistry.addRecipe(<output>,
    	"<I1><I2>",
    	"<I3><I4>",
    	<items>
);"""

recipe3x3 = """GameRegistry.addRecipe(<output>,
    	"<I1><I2><I3>",
    	"<I4><I5><I6>",
      "<I7><I8><I9>",
    	<items>
);"""

recipeItems = """'<i>', <instancename>"""

imports = """import net.minecraft.item.ItemStack;"""