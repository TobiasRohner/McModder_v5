# -*- coding: utf-8 -*-
recipeShapeless = """GameRegistry.addShapelessRecipe(<output>, <imputs>);"""

recipeShaped = """GameRegistry.addRecipe(<output>,
<grid>,
<items>
);"""

recipeItems = """'<i>', <instancename>"""

imports = ["""import net.minecraft.item.ItemStack;""",
           """import net.minecraft.init.Items;""",
           """import net.minecraft.init.Blocks;"""]