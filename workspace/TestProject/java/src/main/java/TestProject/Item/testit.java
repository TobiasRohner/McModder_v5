package TestProject.Item;

import net.minecraft.item.Item;
import net.minecraftforge.fml.common.registry.GameRegistry;
import TestProject.TestProject;
import net.minecraft.creativetab.CreativeTabs;

public class testit extends Item{

private final String name = "testit";

    public testit() {
        GameRegistry.registerItem(this, name);
        this.setUnlocalizedName(name);
        this.setCreativeTab(CreativeTabs.tabMisc);
    }
	
	public String getName() {
		return name;
	}

}